import { printReceived, matcherHint } from "jest-matcher-utils";
import { PASS_SCORE } from "../../models/result";
import { Specification } from "../../models/specification";
import { getDataFromCli } from "../../parser";
import { compactObject, isSameStory } from "../utils";

export async function toBeSameStory(original: Specification) {
  const passMessage =
    matcherHint(".not.toBeSameStory", "received", "") +
    "\n\n" +
    `Expected the stories to be the same ${printReceived(original)} but received:\n` +
    `  ${printReceived(original)}`;

    let failMessage =
      matcherHint(".toBeSameStory", "received", "") +
      "\n\n" +
      "It's not the same story:\n" +
      `  ${printReceived(original)}`;
    
  let pass: boolean;

  console.info("Please wait for some time. It might take several mins to complete.");
  
  try {
    const { success, result } = await getDataFromCli(compactObject(original) as Specification);

    if (result && success) {
      pass = isSameStory(result.results?.MAE + "");
      
      if (!pass) {
        failMessage =
        matcherHint(".toBeSameStory", "received", "") +
        "\n\n" +
        `It's not the same story. The received MAE (mean absolute error) ${result.results?.MAE} is higher than the threshold value (${PASS_SCORE}). \n` + 
        `The url for the original image: \n ${result.results?.url_check_frame}`;
        `The url for the storycap captured image: \n ${result.results?.url_screenshot}`;
        `The url for the blue difference image for the MAE calculation: \n ${result.results?.url_blue_difference}`;
        `The url for the gray difference image for the MAE calculation: \n ${result.results?.url_gray_difference}`;
      }
    } else {
      pass = false;
    }
  } catch (error) {
    pass = false;
  }


  return { pass, message: () => (pass ? passMessage : failMessage) };
}
