"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.toBeSameStory = void 0;
const jest_matcher_utils_1 = require("jest-matcher-utils");
const parser_1 = require("../../parser");
const utils_1 = require("../utils");
async function toBeSameStory(original) {
    var _a;
    const passMessage = (0, jest_matcher_utils_1.matcherHint)(".not.toBeSameStory", "received", "") +
        "\n\n" +
        `Expected the stories to be the same ${(0, jest_matcher_utils_1.printReceived)(original)} but received:\n` +
        `  ${(0, jest_matcher_utils_1.printReceived)(original)}`;
    const failMessage = (0, jest_matcher_utils_1.matcherHint)(".toBeSameStory", "received", "") +
        "\n\n" +
        "Expected the stories to be the same but received:\n" +
        `  ${(0, jest_matcher_utils_1.printReceived)(original)}`;
    let pass;
    console.info("Please wait for some time. It might take several mins to complete.");
    try {
        const { success, result } = await (0, parser_1.getDataFromCli)((0, utils_1.compactObject)(original));
        console.log("result=====>", result);
        if (result && success) {
            pass = (0, utils_1.isSameStory)(((_a = result.results) === null || _a === void 0 ? void 0 : _a.MAE) + "");
        }
        else {
            pass = false;
        }
    }
    catch (error) {
        pass = false;
    }
    return { pass, message: () => (pass ? passMessage : failMessage) };
}
exports.toBeSameStory = toBeSameStory;
