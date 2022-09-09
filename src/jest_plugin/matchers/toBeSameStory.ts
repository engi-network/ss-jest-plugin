import { printReceived, matcherHint } from "jest-matcher-utils";
import { Specification } from "../../models/specification";
import { getDataFromCli } from "../../parser";
import { isSameStory } from "../utils";

export async function toBeSameStory(original: Specification) {
  const passMessage =
    matcherHint(".not.toBeSameStory", "received", "") +
    "\n\n" +
    `Expected the stories to be the same ${printReceived(original)} but received:\n` +
    `  ${printReceived(original)}`;

  const failMessage =
    matcherHint(".toBeSameStory", "received", "") +
    "\n\n" +
    "Expected the stories to be the same but received:\n" +
    `  ${printReceived(original)}`;
  
  let pass: boolean;

  try {
    const { result: data } = await getDataFromCli();
    if (data && data.results) {
      pass = isSameStory(data.results.MAE + "");
    } else {
      pass = false;
    }
  } catch (error) {
    pass = false;
  }


  return { pass, message: () => (pass ? passMessage : failMessage) };
}
