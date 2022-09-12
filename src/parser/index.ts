import { spawn } from "child_process";
import {  formatSpecToCliOptions } from "../jest_plugin/utils";
import { MessageData, CliResult } from "~/models/result";
import { Specification } from "~/models/specification";

export function getDataFromCli(data: Specification): Promise<CliResult> {
  const { dataPath, repository } = data;
  
  const options = formatSpecToCliOptions(data);

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
      "staging"]
      );


  return new Promise((resolve, reject) => {
    let result;

    job.stdout.on("data", (data: ArrayLike<number>) => {
      try {
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
      
      console.log("result=======>", messageData);
  
      } catch (error) {
        reject(new Error("Something went wrong!"));
      }
    });
    
    job.stderr.on("data", (data) => {
      console.log(`Info data=====> ${data}`);
      // INFO logs come here
    });
  
    job.on("close", () => {
      // if (code === 0) {
      //   console.log("The job has been done successfully.");
      // } else {
      //   console.error(`Something went wrong. The exit code is ${code}`);
      // }

      console.log("ended with======>", result);
      resolve(result);
    });
  });
}

