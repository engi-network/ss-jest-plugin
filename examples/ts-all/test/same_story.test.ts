import {  contactUsData } from "../src/data";

const timeout = 60_000 * 3;

describe("expect same story", () => {
  // test("are they same story?", async () => {
  //   await expect(mockInputData).toBeSameStory();
  // }, timeout);

  test("are they same story?", async () => {
    await expect(contactUsData).toBeSameStory();
  }, timeout);

});
