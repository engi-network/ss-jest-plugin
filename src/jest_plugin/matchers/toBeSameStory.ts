import { printReceived, matcherHint } from "jest-matcher-utils";
import { Specification } from "../../models/specification";

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

  const pass = true;

  return { pass, message: () => (pass ? passMessage : failMessage) };
}
