import { spawn } from "child_process";
import {  formatSpecToCliOptions } from "../jest_plugin/utils";
import { MessageData, CliResult } from "~/models/result";
import { Specification } from "~/models/specification";

export function getDataFromCli(data: Specification): Promise<CliResult> {
  const { dataPath, repository } = data;
  
  const options = formatSpecToCliOptions(data);

  const controller = new AbortController();
  const { signal } = controller;

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
    { signal }
    );


  return new Promise((resolve, reject) => {
    let result;

    job.stdout.on("data", (data: ArrayLike<number>) => {
      try {
        console.log(`${data}`);
        const messageData: MessageData = JSON.parse(`${data}`);
        const { step, step_count, error } = messageData;
  
        if (error) {
          result =  {
            success: false,
            message: "Something went wrong."
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
    
    job.stderr.on("data", (data: ArrayLike<number> ) => {
      // cli INFO logs come here
      console.log(`${data}`);
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

