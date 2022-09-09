import { spawn, execSync } from "child_process";
import { MessageData, CliResult } from "~/models/result";
import { SCRIPT_PATH } from "./constants"; 

const job = spawn(SCRIPT_PATH);

execSync(`chmod -R 777 ${SCRIPT_PATH}`);

export function getDataFromCli(): Promise<CliResult> {
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
  
        console.log(messageData);
  
        if (step === step_count - 1) {
          result = {
            success: true,
            result: messageData
          };
        }
  
      } catch (error) {
        console.error("The engi cli data can not be parsed.");
        reject(new Error("Something went wrong!"));
      }
    });
    
    job.stderr.on("data", (data: ArrayLike<number>) => {
      console.error("From error channel:", `${data}`);
    });
  
    job.on("close", (code: number) => {
      if (code === 0) {
        console.log("The job has been done successfully.");
      } else {
        console.error(`Something went wrong. The exit code is ${code}`);
      }
  
      resolve(result);
    });
  });
}

