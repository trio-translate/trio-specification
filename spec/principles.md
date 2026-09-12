# Product principles

Status: Draft

1. **Optimize for understanding.** A successful API response is not proof that people understood one another. Make clarification and correction part of the core journey.
2. **Give every participant control.** Listening, speaking, playback, stopping, and sharing must be understandable from each person's position.
3. **Preserve the speaker's meaning.** Do not silently improve, soften, intensify, summarize, or add claims to translated speech.
4. **Make uncertainty actionable.** Offer a repeat, correction, or clarification path. Do not use an unexplained confidence score to imply certainty.
5. **Make failure recoverable.** Preserve active session intent and useful participant outcomes, recover automatically from recoverable faults, and explain capability gaps without duplicate speech or hidden capture. A routine restart workaround is not graceful recovery.
6. **Use the least data necessary.** Retention and sharing are explicit product choices. Content is not an analytics shortcut.
7. **Deliver one complete situation first.** A narrow release that works end to end is more useful than many incomplete modes.
8. **Earn paid use through value.** Packaging should make cost and limits understandable without trapping people during a conversation.
9. **Expand using evidence.** Add languages, modes, vendors, and infrastructure when quality, demand, or economics justify the burden.
10. **Start once and keep working.** The [agreed continuity contract](non-negotiables.md) requires twelve-hour unattended operation and a predefined timeout based on conversation words. Noise and internal service limits must not randomly end the session.

When principles conflict, document the concrete tradeoff in a [decision record](decisions/README.md). For example, optional conversation history may improve continuity but increases retention and access responsibilities.
