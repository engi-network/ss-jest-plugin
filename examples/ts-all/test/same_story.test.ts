import { mockInputData, contactUsData } from "../src/data";

const timeout = 60_000 * 5;

describe("Expect same story", () => {
  test.concurrent("Are they the same story?", async () => {
    await expect(mockInputData).toBeSameStory();
  }, timeout);

  test.concurrent("Is Contact page the same story?", async () => {
    await expect(contactUsData).toBeSameStory();
  }, timeout);

});
