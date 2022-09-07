import * as matchers from "../matchers";

console.log("========>");
const jestExpect = expect;

if (jestExpect !== undefined) {
  console.log("========>");
  expect.extend(matchers);
} else {
  throw new Error(
    "Unable to find Jest's global expect. " +
      "Please check you have added jest-extended correctly to your jest configuration. " +
      "See https://github.com/jest-community/jest-extended#setup for help.",
  );
}
