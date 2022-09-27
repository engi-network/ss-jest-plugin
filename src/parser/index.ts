import { spawn } from "child_process";
import {  formatSpecToCliOptions } from "../jest_plugin/utils";
import { MessageData, CliResult } from "~/models/result";
import { Specification } from "~/models/specification";

export function getDataFromCli(spec: Specification): Promise<CliResult> {
  const { dataPath, repository, debug } = spec;
  
  const options = formatSpecToCliOptions(spec);

  const job = spawn(
    "pipenv",
    [
      "run",
      "engi",
      "submission",
      "execute",
      `${dataPath}`,
      "figma",
      `${repository}`,
      ...options,
      "--env",
      "staging"
    ],
    );


  return new Promise((resolve, reject) => {
    let result;

    job.stdout.on("data", (data: ArrayLike<number>) => {
      try {
        const messageData: MessageData = JSON.parse(`${data}`);
        const { step, step_count, error } = messageData;
  
        if (error) {
          const errorMessage = Object.values(error).reduce((prev, current) => { prev = prev + "\n" + current; return prev;}, "");

          result =  {
            success: false,
            message: errorMessage
          };
        }

        if (step === step_count - 1) {
          result = {
            success: true,
            result: messageData
          };
        }
      } catch (error) {
        if (!(data + "")) {
          result = {
            success: false,
            message: "Nothing to parse from cli."
          };
        }
      }
    });
    
    job.stderr.on("data", (data: ArrayLike<number>) => {
      if (debug) {
        console.log(`${data}`);
      }
    });
  
    job.on("close", (code) => {
      if (code === 0) {
        resolve(result);
      } else {
        reject(result);
      }
    });
  });
}

