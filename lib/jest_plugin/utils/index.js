"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.compactObject = exports.formatSpecToCliOptions = exports.formatArgs = exports.isSameStory = void 0;
const result_1 = require("../../models/result");
function isSameStory(mae) {
    return Number(mae.split(" ")[0]) < result_1.PASS_SCORE;
}
exports.isSameStory = isSameStory;
function formatArgs(args) {
    return args.reduce((prev, { name, value }) => {
        prev.push("--knob");
        prev.push(`${name}=${value}`);
        return prev;
    }, []);
}
exports.formatArgs = formatArgs;
const whitelistKeys = ["component", "height", "path", "story", "width", "args"];
function formatSpecToCliOptions(data) {
    return Object.entries(data).reduce((prev, [key, value]) => {
        if (!whitelistKeys.includes(key) || typeof value === "undefined") {
            return prev;
        }
        if (key === "args") {
            const knobs = formatArgs(value);
            prev = [...prev, ...knobs];
            return prev;
        }
        prev.push(`--${key}`);
        prev.push(value + "");
        return prev;
    }, []);
}
exports.formatSpecToCliOptions = formatSpecToCliOptions;
function compactObject(val) {
    const data = Array.isArray(val) ? val.filter(Boolean) : val;
    return Object.keys(data).reduce((acc, key) => {
        const value = data[key];
        if (Boolean(value))
            acc[key] = typeof value === "object" ? compactObject(value) : value;
        return acc;
    }, Array.isArray(val) ? [] : {});
}
exports.compactObject = compactObject;
