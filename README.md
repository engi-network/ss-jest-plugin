# Same Story? Jest Plugin

## What is this for?

This package is Jest plugin which runs in Jest context and let users to write a test to compare their work result against figma exported images. The way it works is similar to Figma plugin for same story but for Jest.

## Prerequisite

1. Please install the package by running this command. `npm i -D same-story-jest-plugin`.
1. Please install `pipenv` cli because this is based on Python cli.
1. Please export png file from figma that you are going to compare with a correct name. That is the value for "dataPath" in your test input data for `toBeSameStory` matcher.

## Setup for jest.

1. Please create a `jest.setup.ts` and copy the following code.

```javascript
import { toBeSameStory } from 'same-story-jest-plugin/lib'

expect.extend({ toBeSameStory })
```

2. Include `jest.setup.ts` to your `jest.config.js` file.

```javascript
  module.exports = {
    roots: ["<rootDir>"],
    ...
    setupFilesAfterEnv: ["<rootDir>/jest.setup.ts"],
  };
```
