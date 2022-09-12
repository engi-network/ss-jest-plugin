import { DFormValues, Specification } from "../../models/specification";
import { PASS_SCORE } from "../../models/result";

export function isSameStory(mae: string): boolean {
  return Number(mae.split(" ")[0]) < PASS_SCORE;
}

export function formatArgs(args: DFormValues): Array<string> {
  return args.reduce((prev, {name, value}) => {
    prev.push("--knob");
    prev.push(`${name}=${value}`);
    
    return prev;
  }, [] as Array<string>);
}

const whitelistKeys = ["component", "height", "path", "story", "width", "args"];

export function formatSpecToCliOptions(data: Specification): Array<string> {
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
  }, [] as Array<string>);
}

export  function compactObject(val){
  const data = Array.isArray(val) ? val.filter(Boolean) : val;
  
  return Object.keys(data).reduce(
    (acc, key) => {
      const value = data[key];
      if (Boolean(value))
        acc[key] = typeof value === "object" ? compactObject(value) : value;
      return acc;
    },

    Array.isArray(val) ? [] : {}
  );
}