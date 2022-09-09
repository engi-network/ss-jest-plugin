import { PASS_SCORE } from "../../models/result";

export function isSameStory(mae: string): boolean {
  return Number(mae.split(" ")[0]) < PASS_SCORE;
}
