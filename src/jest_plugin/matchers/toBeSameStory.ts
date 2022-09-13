import { printReceived, matcherHint } from "jest-matcher-utils";
import { Specification } from "../../models/specification";
import { getDataFromCli } from "../../parser";
import { compactObject, isSameStory } from "../utils";

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

  console.info("Please wait for some time. It might take several mins to complete.");
  
  try {
    const { success, result } = await getDataFromCli(compactObject(original) as Specification);

    if (result && success) {
      pass = isSameStory(result.results?.MAE + "");
    } else {
      pass = false;
    }
  } catch (error) {
    pass = false;
  }


  return { pass, message: () => (pass ? passMessage : failMessage) };
}
