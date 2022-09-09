module.exports = {
  roots: ["<rootDir>"],
  preset: "ts-jest",
  testRegex: "test/.*\\.test\\.tsx?$",
  moduleFileExtensions: ["ts", "tsx", "js"],
  setupFilesAfterEnv: ["<rootDir>/jest.setup.ts"],
};
