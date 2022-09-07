# Engi CLI

## Install

```
pipenv install -d
```

### Linguist

```
gem install github-linguist --bindir /usr/local/bin
```

### Build a Docker image on a Mac

Running Docker from within Docker :exploding_head:

```
docker compose build --ssh default
TMPDIR=/tmp docker compose up
```

### Generate Python requirements

```
pipenv requirements --dev | grep -v "^git" >requirements.txt
```

## Testing

```
pipenv run pytest -s
```

## Run

### List available commands

```
pipenv run engi --help
```

### Get help for a specific command

Example:
```
pipenv run engi health --help
```

### Job submission

#### Figma

Assuming the source for [same-story-api](https://github.com/engi-network/same-story-api) is at `../same-story-api`

##### Environment

Currently, the command is using AWS credentials via boto3.

##### Submit a job, receive results

```
pipenv run engi submission execute ../same-story-api/test/data figma engi-network/same-story-storybook --env staging
```

| Argument    | Description |
| ----------- | ----------- |
| `../same-story-api/test/data` | a directory containing the check frame image exported from Figma |
| `figma` | tells the CLI to execute a `same-story-api` job |
| `engi-network/same-story-storybook` | the GitHub repo containing the Storybook |