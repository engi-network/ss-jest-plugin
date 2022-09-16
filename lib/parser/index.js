"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getDataFromCli = void 0;
const child_process_1 = require("child_process");
const utils_1 = require("../jest_plugin/utils");
function getDataFromCli(spec) {
    const { dataPath, repository, debug } = spec;
    const options = (0, utils_1.formatSpecToCliOptions)(spec);
    const job = (0, child_process_1.spawn)("pipenv", [
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
    ]);
    return new Promise((resolve, reject) => {
        let result;
        job.stdout.on("data", (data) => {
            try {
                const messageData = JSON.parse(`${data}`);
                const { step, step_count, error } = messageData;
                if (error) {
                    result = {
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
            }
            catch (error) {
                if (!(data + "")) {
                    result = {
                        success: false,
                        message: "Nothing to parse from cli."
                    };
                }
            }
        });
        job.stderr.on("data", (data) => {
            // cli INFO logs come here
            if (debug) {
                console.log(`${data}`);
            }
        });
        job.on("close", (code) => {
            if (code === 0) {
                resolve(result);
            }
            else {
                reject(result);
            }
        });
    });
}
exports.getDataFromCli = getDataFromCli;
