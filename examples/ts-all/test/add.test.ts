describe("expect same story", () => {
  test("are they same story?", () => {
    expect(new Date("2023/10/7")).toBeSameStory(new Date());
  });
});
