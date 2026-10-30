---
name: td-mcp-bootstrap
description: Automatically prepare new TouchDesigner projects with Kuanfu Weimu's local TDMCP component, start its service, and verify the MCP connection without dragging files or controlling the screen. Use before creating a new TD project or when TD MCP is disconnected.
---

# TD MCP bootstrap

Use this workflow automatically for agent-created TD projects. A skill is not a hook into TouchDesigner's File > New command. Do not promise that manually created projects already contain TDMCP.

Default source: `D:\Derivative\TouchDesigner.2025.32460\Samples\Palette\TDMCP.tox`.
Default executable: `D:\Derivative\TouchDesigner.2025.32460\bin\TouchDesigner.exe`.
Keep scratch, generated components, and projects on D. Never edit the source plugin or installed TD files. Do not use mouse/keyboard/UI automation. Launches use a hidden window and never close unrelated TD processes.

## New project

Run `D:\Python\python.exe <skill>/scripts/bootstrap.py --output-dir <new-project-folder> --name <project-name> --launch`.
The script expands a copy with TD's own tools, enables Active, disables viewport-follow/highlight to respect the no-screen-control preference, and preserves authentication settings. It checks the actual plugin save build against the installed build before launching. It will not overwrite existing files.

On success it initializes MCP, lists tools, calls read-only project_info, checks that this is the intended new project, then saves the new `.toe` via save_project. Inspect get_errors before beginning creative work. Retain the generated bootstrap JSON receipt. This method needs no pre-existing MCP connection.

If another process owns the configured port, stop instead of connecting to an arbitrary project. Existing-project work must use the already connected, identity-verified project or an authorized copy; never launch a new empty project and present it as the user's existing work. For a connected existing project, inspect whether TDMCP is already present before loading anything.

## Failures and authorization

- Version conflict: report the plugin save build and installed build; use a compatible installation/component. Never patch the saved build number to hide the conflict. Do not repeat launches or ask the user to drag the same file again.
- Authentication: preserve it; use the host's legitimate OAuth flow. A required consent cannot be bypassed. This local 1.1.54 file has Auth off by default, but do not assume future files do.
- Timeout: report only the created files and failed live verification. Do not claim connected or create duplicate processes. The returned PID identifies only the helper-created instance.
- A 200 response or open port is not proof of an MCP connection. Require initialize + tools/list + project_info and project identity before mutations.

For the film project, retain its stage and aesthetic approval gates; configuring this helper does not approve later film stages.

## Verified local state (2026-10-31)

Source TDMCP is 1.1.54, saved in 2025.33070, with Active default off. Installed TD is 2025.32460. An isolated launch hit `File load version conflict`; no MCP project_info succeeded. The isolated test process was stopped; the user's original TD process was left running. Offline preparation and version rejection are tested; live startup/save remain unverified until compatible versions are available.

Official utility documentation: https://docs.derivative.ca/Toeexpand and https://docs.derivative.ca/Toecollapse .
