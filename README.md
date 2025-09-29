# PulseScope watchOS and iOS app
A privacy-first contextual stress & recovery app for Apple Watch with real-time micro-coaching and next-day recovery scoring.
## Tooling choices
	•	SwiftUI everywhere; no UIKit unless absolutely necessary.
	•	Core ML Tools to quantize tiny models. Accelerate for simple DSP if needed.
	•	Unit tests for feature extraction and fusion logic; UITests for watch flows.