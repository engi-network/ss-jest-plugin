# Same Story? Jest Plugin

## What is this for?

This package is Jest plugin which runs in Jest context and let users to write a test to compare their work result against figma exported images. The way it works is similar to Figma plugin for same story but for Jest.

## Prerequisite

1. Please install pipenv cli because this is based on Python cli.
2. Please export png file from figma that you are going to compare with a correct name. That is the value for "dataPath" in your test input data for "toBeSameStory" matcher.
