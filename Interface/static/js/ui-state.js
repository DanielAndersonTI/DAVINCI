"use strict";

// Pure selection state for the configuration and AI selectors. The DOM-free
// module is loaded by the page and can also be required by Node tests.
(function (root, factory) {
	const api = factory();
	if (typeof module !== "undefined" && module.exports) {
		module.exports = api;
	} else {
		root.DavinciState = api;
	}
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
	const FIELDS = ["configuration", "provider", "keyNumber"];

	function normalize(initial) {
		return {
			configuration: initial.configuration,
			provider: initial.provider,
			keyNumber: typeof initial.keyNumber === "number" ? initial.keyNumber : null,
		};
	}

	function createSelectionState(initial) {
		let confirmed = normalize(initial);
		let pending = normalize(initial);

		return {
			confirmed() {
				return { ...confirmed };
			},
			pending() {
				return { ...pending };
			},
			set(field, value) {
				if (!FIELDS.includes(field)) return false;
				pending[field] = value;
				return true;
			},
			setProvider(provider, keyNumber) {
				pending.provider = provider;
				pending.keyNumber = typeof keyNumber === "number" ? keyNumber : null;
			},
			isDirty() {
				return FIELDS.some((field) => pending[field] !== confirmed[field]);
			},
			confirm() {
				confirmed = { ...pending };
				return { ...confirmed };
			},
			discard() {
				pending = { ...confirmed };
				return { ...confirmed };
			},
			reset(next) {
				confirmed = normalize(next);
				pending = { ...confirmed };
				return { ...confirmed };
			},
		};
	}

	return { createSelectionState };
});
