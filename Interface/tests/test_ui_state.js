"use strict";

// Dependency-free checks for the pure selector state used by the interface.
const assert = require("assert");
const path = require("path");

const stateModule = require(path.join(__dirname, "..", "static", "js", "ui-state.js"));
const { createSelectionState } = stateModule;

let checks = 0;
const check = (condition, message) => {
	assert.ok(condition, message);
	checks += 1;
};

const base = { configuration: "c1", provider: "deepseek", keyNumber: 1 };
let state = createSelectionState(base);

assert.deepStrictEqual(state.confirmed(), base);
assert.deepStrictEqual(state.pending(), base);
check(!state.isDirty(), "a fresh state is not dirty");

check(state.set("configuration", "c3") === true, "a known field can be changed");
check(state.pending().configuration === "c3", "the pending value changes");
check(state.confirmed().configuration === "c1", "the confirmed value does not change");
check(state.isDirty(), "a pending change marks the state dirty");

assert.deepStrictEqual(state.discard(), base);
check(!state.isDirty(), "discard restores the confirmed value");

state.set("configuration", "c4");
state.setProvider("gemini", 2);
assert.deepStrictEqual(state.pending(), { configuration: "c4", provider: "gemini", keyNumber: 2 });
assert.deepStrictEqual(state.confirm(), { configuration: "c4", provider: "gemini", keyNumber: 2 });
check(!state.isDirty(), "confirm adopts the pending values");
check(state.confirmed().provider === "gemini", "the provider is confirmed");
check(state.set("unknown", "value") === false, "unknown fields are ignored");
state.setProvider("claude", 2);
check(state.pending().keyNumber === 2, "setProvider adopts a numeric key");

state.setProvider("claude", null);
check(state.pending().keyNumber === null, "setProvider with null clears the key");
check(state.isDirty(), "a provider without a key is a pending change");

const reset = state.reset({ configuration: "c0", provider: "deepseek", keyNumber: 1 });
assert.deepStrictEqual(reset, { configuration: "c0", provider: "deepseek", keyNumber: 1 });
check(!state.isDirty(), "reset clears the pending change");

console.log(`ui-state: ${checks} checks passed`);
