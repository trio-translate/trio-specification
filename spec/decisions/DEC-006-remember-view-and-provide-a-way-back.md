# DEC-006: Remember the last view and always provide a way back

Status: Agreed outcomes; restoration/navigation details Draft
Date: 2026-09-12
Decision owner: Product owner

## Decision and evidence

The product owner requires the last view to be remembered and a way to get back to always be available.

## Working interpretation

- Restore the last applicable view when returning to or reopening Trio. Persist the view preference locally so it works offline.
- Every app-owned secondary screen, detail, dialog, overlay, and full-screen mode has an understandable back/close route. At a root or direct entry without history, provide a stable route to the main conversation/home view rather than a dead end.
- Ordinary navigation within Trio preserves an active session and its persistent microphone/stop controls. Back is not an implicit stop/end action.
- Restoring layout/view is separate from resuming capture, reconstructing deleted/transient content, or rejoining a room. A cold relaunch never starts the microphone solely because a live view was remembered.
- If the remembered view is unavailable, deleted, unsupported, or no longer authorized, use a documented safe fallback. Explain that outside participant text areas.

Exact view identity, per-device/account synchronization, scroll restoration, and handling of temporary dialogs remain design details. Remembering the last durable view is the proposed baseline; transient error/permission dialogs should not trap the user on return.

Affected requirements: FR-022/FR-023. See [navigation design](../experience/interaction-design.md#navigation-and-view-restoration) and [validation](../delivery/validation-and-acceptance.md).

Supersedes: None.
