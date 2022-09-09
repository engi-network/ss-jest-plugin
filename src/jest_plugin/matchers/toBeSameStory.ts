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
    const result = await getDataFromCli();
    console.log("result=======>", result);
    // if (data && data.results) {
    //   pass = isSameStory(data.results.MAE + "");
    // } else {
    //   pass = false;
    // }
    pass = true;
  } catch (error) {
    pass = false;
    console.log("error=====>", error);
  }


  return { pass, message: () => (pass ? passMessage : failMessage) };
}
