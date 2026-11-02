# Store Readiness (App Store / Play Store)

Only for apps submitted to a store. Status: `verificado` = confirmed in official source on 2026-10-12.

| Item | Rule | Status |
|---|---|---|
| Demo account | Give App Review an active demo account (or full demo mode) with pre-populated data, and explain non-obvious features and in-app purchases in the review notes | verificado (developer.apple.com/app-store/review/guidelines) |
| Account deletion | If the app supports account creation, offer account deletion **inside the app** (Apple 5.1.1(v)). Google Play also requires it in-app **and** a web link where users can request deletion, disclosed in the Data safety form | verificado (Apple guidelines; support.google.com/googleplay/android-developer/answer/13327111 and answer/10144311, 2026-10-12) |
| In-app purchase | Unlocking features or subscriptions uses in-app purchase; have a restore mechanism | verificado (Apple 3.1.1) |
| Restore purchases | Reinstall from scratch, sign in, confirm the entitlement returns | procedure, test on device |
| Production keys | Swap sandbox/test payment and API keys for production in the final build; grep the build config for `test`/`sandbox` | procedure |
| Phased rollout | Apple: "Phased Release for Automatic Updates" releases the update gradually over 7 days and can be paused or resumed; the percentages are Apple's, not configurable. Google Play staged rollout percentages: não verificado | Apple verificado 2026-10-12 (developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases); Google não verificado |
| Privacy labels | Declare what each SDK collects in App Privacy / Data safety; must match the real network calls. Google: all data collected per the Data safety section is within scope of account deletion | Apple: ver guidelines 5.1; Google: parcial, verificado 2026-10-12 (answer/13327111) |
| Brazil minors | ECA Digital applies to apps likely to be accessed by minors; app stores must provide an age signal API (Lei 15.211/2025, art. 12, verificado, planalto.gov.br) | verificado |
| Friday rule | Do not submit or release on a Friday | recomendação operacional, sem fonte legal |

## Pre-submit run

1. Build the release candidate, install on a clean device.
2. Sign up with a brand-new Gmail (no cached state), complete the core flow, delete the account from inside the app.
3. Reinstall, restore purchases.
4. Confirm privacy policy URL opens without login.
5. Put the demo credentials and chatbot explanation (if any) in the review notes.
