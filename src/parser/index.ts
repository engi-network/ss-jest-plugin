import { spawn, execSync } from "child_process";
import { MessageData } from "~/parser/models/result";
import { SCRIPT_PATH } from "./constants"; 

const job = spawn(SCRIPT_PATH);

execSync(`chmod -R 777 ${SCRIPT_PATH}`);

job.stdout.on("data", (data: ArrayLike<number>) => {
  try {
    const messageData: MessageData = JSON.parse(`${data}`);

    console.log(messageData);
  } catch (error) {
    console.error("The python cli data can not be parsed.");
  }
});

job.stderr.on("data", (data: ArrayLike<number>) => {
  console.error(`${data}`);
});

job.on("close", (code: number) => {
  if (code === 0) {
    console.log("The job has been done successfully.");
  } else {
    console.error(`Something went wrong. The exit code is ${code}`);
  }
});
