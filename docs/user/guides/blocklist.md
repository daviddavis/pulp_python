# Package Blocklist

A repository can have a blocklist that prevents specific packages from being added.
Blocklist entries can match by package `name` (all versions), package `name` with an exact `version`, or exact `filename`.
Exactly one of `name` or `filename` must be provided.

Each entry records the PRN of the user who created it in the `added_by` field.

## Setup

If you do not already have a repository, create one:

```bash
pulp python repository create --name foo
```

Set the API base URL and repository HREF for use in the subsequent commands:

```bash
PULP_API="http://localhost:5001"
REPO_HREF=$(pulp python repository show --name foo | jq -r ".pulp_href")
```

## Add a blocklist entry

=== "By name (all versions)"

    ```bash
    # Block all versions of shelf-reader
    http POST "${PULP_API}${REPO_HREF}blocklist_entries/" name="shelf-reader"
    ```

=== "By name and version"

    ```bash
    # Block only shelf-reader 0.1
    http POST "${PULP_API}${REPO_HREF}blocklist_entries/" name="shelf-reader" version="0.1"
    ```

=== "By filename"

    ```bash
    # Block only shelf-reader-0.1.tar.gz
    http POST "${PULP_API}${REPO_HREF}blocklist_entries/" filename="shelf-reader-0.1.tar.gz"
    ```

Set the UUID of a created entry for use in the subsequent commands:

```bash
ENTRY_UUID=$(http GET "${PULP_API}${REPO_HREF}blocklist_entries/" | jq -r '.results[0].prn | split(":") | .[-1]')
```

## List blocklist entries

List all entries for a repository:

```bash
http GET "${PULP_API}${REPO_HREF}blocklist_entries/"
```

Show a single entry:

```bash
http GET "${PULP_API}${REPO_HREF}blocklist_entries/${ENTRY_UUID}/"
```

## Remove a blocklist entry

```bash
http DELETE "${PULP_API}${REPO_HREF}blocklist_entries/${ENTRY_UUID}/"
```

Once an entry is removed, packages matching it can be added to the repository again.
