"use strict";

document.addEventListener("DOMContentLoaded", () => {
	const template = document.querySelector("#system-block-template");
	const systemsContainer = document.querySelector("#systems-container");
	const addButton = document.querySelector("#add-system-button");
	const countLabel = document.querySelector("#system-count");
	const runButton = document.querySelector("#run-button");
	const globalAlert = document.querySelector("#global-alert");
	const loadingAlert = document.querySelector("#pipeline-loading");
	const progressBar = document.querySelector("#pipeline-progress-bar");
	const progressPercent = document.querySelector("#pipeline-percent");
	const progressStatus = document.querySelector("#pipeline-status");
	const inputView = document.querySelector("#input-view");
	const resultsView = document.querySelector("#results-view");
	const runSettingsSummary = document.querySelector("#run-settings-summary");
	const newDecompositionButton = document.querySelector("#new-decomposition-button");
	const rerunExperimentButton = document.querySelector("#rerun-experiment-button");
	const downloadReportButton = document.querySelector("#download-report-button");
	const downloadSpecificationButton = document.querySelector("#download-specification-button");
	const configurationToggle = document.querySelector("#configuration-toggle");
	const configurationCurrent = document.querySelector("#configuration-current");
	const configurationMenu = document.querySelector("#configuration-menu");
	const providerToggle = document.querySelector("#provider-toggle");
	const providerCurrent = document.querySelector("#provider-current");
	const providerMenu = document.querySelector("#provider-menu");
	const providerOptions = document.querySelector("#provider-options");
	const keyStatus = document.querySelector("#key-status");
	const keyOptions = document.querySelector("#key-options");
	const newApiKeyInput = document.querySelector("#new-api-key");
	const saveKeyButton = document.querySelector("#save-key-button");
	const setActiveKeyCheckbox = document.querySelector("#set-active-key");
	const keyFeedback = document.querySelector("#key-feedback");
	const confirmBackdrop = document.querySelector("#confirm-backdrop");
	const confirmMessage = document.querySelector("#confirm-message");
	const confirmAccept = document.querySelector("#confirm-accept");
	const confirmDiscard = document.querySelector("#confirm-discard");
	if (!template || !systemsContainer) return;

	let settingsPayload = null;
	let selection = null;
	let openMenu = null;
	let afterConfirm = null;

	const showAlert = (message, type = "danger") => {
		globalAlert.className = `alert alert-${type}`;
		globalAlert.textContent = message;
		globalAlert.scrollIntoView({ behavior: "smooth", block: "nearest" });
	};

	const clearAlert = () => {
		globalAlert.className = "alert d-none";
		globalAlert.textContent = "";
	};

	const providerEntry = (providerId) => {
		if (!settingsPayload) return null;
		return settingsPayload.providers.find((provider) => provider.id === providerId) || null;
	};

	const providerLabel = (providerId) => {
		const provider = providerEntry(providerId);
		if (provider) return provider.label;
		return providerId === "gemini" ? "Gemini" : providerId === "claude" ? "Claude" : "DeepSeek";
	};

	const keyLabel = (providerId, number) => {
		const provider = providerEntry(providerId);
		if (!provider || typeof number !== "number") return "";
		const key = provider.keys.find((item) => item.number === number);
		return key ? `${provider.label} ${key.label}` : "";
	};

	const defaultKeyFor = (providerId) => {
		const provider = providerEntry(providerId);
		if (!provider || provider.keys.length === 0) return null;
		const active = provider.keys.find((key) => key.active);
		return active ? active.number : provider.keys[0].number;
	};

	// ---------------------------------------------------------------- settings
	const loadSettings = async () => {
		try {
			const response = await fetch("/api/settings", { cache: "no-store" });
			if (!response.ok) throw new Error("The run settings could not be loaded.");
			settingsPayload = await response.json();
		} catch (error) {
			settingsPayload = null;
			showAlert("The run settings could not be loaded. Reload the page before running the pipeline.");
		}
		if (!settingsPayload) {
			selection = window.DavinciState.createSelectionState({ configuration: "c1", provider: "deepseek", keyNumber: null });
			return;
		}
		const keyNumber = defaultKeyFor(settingsPayload.provider);
		selection = window.DavinciState.createSelectionState({
			configuration: settingsPayload.configuration,
			provider: settingsPayload.provider,
			keyNumber,
		});
	};

	const reloadSettings = async () => {
		if (!selection) return;
		try {
			const response = await fetch("/api/settings", { cache: "no-store" });
			if (!response.ok) return;
			settingsPayload = await response.json();
			selection.reset({
				configuration: settingsPayload.configuration,
				provider: settingsPayload.provider,
				keyNumber: defaultKeyFor(settingsPayload.provider),
			});
		} catch (error) {
			// Keep the values already on screen when the refresh fails.
		}
	};

	const storeSelection = async (payload) => {
		const response = await fetch("/api/settings", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			cache: "no-store",
			body: JSON.stringify(payload),
		});
		const body = await response.json().catch(() => ({}));
		if (!response.ok || !body.ok) throw new Error(body.message || "The selection could not be saved.");
		return body;
	};

	// ------------------------------------------------------------------- menus
	const setMenu = (name) => {
		openMenu = name;
		configurationMenu.classList.toggle("d-none", name !== "configuration");
		providerMenu.classList.toggle("d-none", name !== "provider");
		configurationToggle.setAttribute("aria-expanded", String(name === "configuration"));
		providerToggle.setAttribute("aria-expanded", String(name === "provider"));
	};

	const buildConfigurationMenu = () => {
		configurationMenu.innerHTML = "";
		if (!settingsPayload) return;
		const pendingValue = selection.pending().configuration;
		settingsPayload.configurations.forEach((item) => {
			const option = document.createElement("button");
			option.type = "button";
			option.className = `setup-option${item.id === pendingValue ? " is-selected" : ""}`;
			option.setAttribute("role", "option");
			option.setAttribute("aria-selected", String(item.id === pendingValue));
			option.dataset.configuration = item.id;
			const title = document.createElement("span");
			title.className = "setup-option-title";
			title.textContent = item.label;
			const copy = document.createElement("span");
			copy.className = "setup-option-copy";
			copy.textContent = item.description;
			option.append(title, copy);
			option.addEventListener("click", () => {
				selection.set("configuration", item.id);
				renderSetup();
			});
			configurationMenu.appendChild(option);
		});
	};

	const buildProviderMenu = () => {
		if (!settingsPayload) return;
		const pending = selection.pending();
		providerOptions.innerHTML = "";
		settingsPayload.providers.forEach((provider) => {
			const option = document.createElement("button");
			option.type = "button";
			option.className = `setup-option${provider.id === pending.provider ? " is-selected" : ""}`;
			option.setAttribute("role", "option");
			option.setAttribute("aria-selected", String(provider.id === pending.provider));
			option.dataset.provider = provider.id;
			const title = document.createElement("span");
			title.className = "setup-option-title";
			title.textContent = provider.label;
			const copy = document.createElement("span");
			copy.className = "setup-option-copy";
			copy.textContent = `Model: ${provider.model}${provider.configured ? "" : " | no key configured"}`;
			option.append(title, copy);
			option.addEventListener("click", () => {
				selection.setProvider(provider.id, defaultKeyFor(provider.id));
				keyFeedback.classList.add("d-none");
				keyFeedback.textContent = "";
				renderSetup();
			});
			providerOptions.appendChild(option);
		});
	};

	const buildKeyOptions = () => {
		if (!settingsPayload) return;
		const pending = selection.pending();
		const provider = providerEntry(pending.provider);
		keyOptions.innerHTML = "";
		if (!provider) {
			keyStatus.textContent = "";
			return;
		}
		if (provider.keys.length === 0) {
			keyStatus.textContent = `${provider.label} has no key yet. Add one below, or choose another AI provider.`;
			return;
		}
		if (provider.keys.length === 1) {
			keyStatus.textContent = `${provider.label} uses ${provider.keys[0].label}. It stays on the server.`;
			return;
		}
		keyStatus.textContent = `${provider.label} has ${provider.keys.length} keys. Choose the key to use with this AI.`;
		provider.keys.forEach((key) => {
			const option = document.createElement("label");
			option.className = "key-option";
			const input = document.createElement("input");
			input.type = "radio";
			input.name = "key-choice";
			input.value = String(key.number);
			input.checked = key.number === pending.keyNumber;
			input.addEventListener("change", () => {
				selection.set("keyNumber", key.number);
				renderSetup();
			});
			const label = document.createElement("span");
			label.textContent = key.label;
			option.append(input, label);
			if (key.active) {
				const tag = document.createElement("span");
				tag.className = "key-active-tag";
				tag.textContent = "ACTIVE";
				option.appendChild(tag);
			}
			keyOptions.appendChild(option);
		});
	};

	const renderSetup = () => {
		if (!selection) return;
		const pending = selection.pending();
		configurationCurrent.textContent = pending.configuration.toUpperCase();
		providerCurrent.textContent = providerLabel(pending.provider);
		buildConfigurationMenu();
		buildProviderMenu();
		buildKeyOptions();
	};

	// ------------------------------------------------------------- confirmation
	const describePending = () => {
		const confirmed = selection.confirmed();
		const pending = selection.pending();
		const parts = [];
		if (pending.configuration !== confirmed.configuration) {
			parts.push(`configuration ${pending.configuration.toUpperCase()}`);
		}
		if (pending.provider !== confirmed.provider) {
			const provider = providerEntry(pending.provider);
			parts.push(`AI provider ${provider ? provider.label : pending.provider}`);
		}
		if (pending.keyNumber !== confirmed.keyNumber && pending.keyNumber !== null) {
			const label = keyLabel(pending.provider, pending.keyNumber);
			if (label) parts.push(label);
		}
		return parts;
	};

	const requestConfirmation = (callback = null) => {
		if (!selection) return;
		if (!selection.isDirty()) {
			setMenu(null);
			if (callback) callback();
			return;
		}
		setMenu(null);
		afterConfirm = callback;
		const parts = describePending();
		confirmMessage.textContent = parts.length
			? `Use ${parts.join(" and ")} for the next runs? Anything already typed in the form is kept.`
			: "Keep the current selection for the next runs?";
		confirmBackdrop.classList.remove("d-none");
		confirmAccept.focus();
	};

	const closeConfirmation = () => {
		confirmBackdrop.classList.add("d-none");
		afterConfirm = null;
	};

	const acceptConfirmation = async () => {
		const confirmed = selection.confirmed();
		const pending = selection.pending();
		const payload = {};
		if (pending.configuration !== confirmed.configuration) payload.configuration = pending.configuration;
		if (pending.provider !== confirmed.provider) payload.provider = pending.provider;
		if (pending.keyNumber !== null && (payload.provider || pending.keyNumber !== confirmed.keyNumber)) {
			payload.provider = pending.provider;
			payload.key_number = pending.keyNumber;
		}
		confirmAccept.disabled = true;
		try {
			if (Object.keys(payload).length > 0) {
				settingsPayload = await storeSelection(payload);
			}
			selection.confirm();
			const callback = afterConfirm;
			closeConfirmation();
			renderSetup();
			if (callback) callback();
		} catch (error) {
			confirmAccept.disabled = false;
			showAlert(error.message || "The selection could not be saved.");
		} finally {
			confirmAccept.disabled = false;
		}
	};

	const discardConfirmation = async () => {
		closeConfirmation();
		renderSetup();
		// A key saved with SAVE KEY is already committed on the server, so the
		// discarded view is rebuilt from the persisted values.
		await reloadSettings();
		renderSetup();
	};

	// ------------------------------------------------------------------- keys
	const saveKey = async () => {
		if (!settingsPayload || !selection) return;
		const key = newApiKeyInput.value;
		if (!key.trim()) {
			keyFeedback.textContent = "Enter an API key before saving.";
			keyFeedback.className = "key-feedback key-feedback-error";
			return;
		}
		const providerId = selection.pending().provider;
		saveKeyButton.disabled = true;
		keyFeedback.className = "key-feedback d-none";
		keyFeedback.textContent = "";
		try {
			const response = await fetch("/api/settings/api-key", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				cache: "no-store",
				body: JSON.stringify({ provider: providerId, key, make_active: setActiveKeyCheckbox.checked }),
			});
			const body = await response.json().catch(() => ({}));
			if (!response.ok || !body.ok) throw new Error(body.message || "The key could not be saved.");
			settingsPayload = body;
			if (body.saved_key && body.saved_key.active) selection.set("keyNumber", body.saved_key.number);
			if (selection.pending().keyNumber === null) selection.set("keyNumber", defaultKeyFor(providerId));
			keyFeedback.textContent = `${body.saved_key.label} saved for ${providerLabel(providerId)}.`;
			keyFeedback.className = "key-feedback key-feedback-ok";
			renderSetup();
		} catch (error) {
			keyFeedback.textContent = error.message || "The key could not be saved.";
			keyFeedback.className = "key-feedback key-feedback-error";
		} finally {
			newApiKeyInput.value = "";
			setActiveKeyCheckbox.checked = false;
			saveKeyButton.disabled = false;
		}
	};

	// ------------------------------------------------------------------- form
	const updateBlocks = () => {
		const blocks = [...systemsContainer.querySelectorAll("[data-system-block]")];
		blocks.forEach((block, index) => {
			const number = index + 1;
			block.querySelector("[data-system-number]").textContent = number;
			block.querySelectorAll("[data-field]").forEach((field) => {
				const fieldName = field.dataset.field;
				field.id = `${fieldName.replaceAll("_", "-")}-${number}`;
				const label = block.querySelector(`label[for^="${fieldName.replaceAll("_", "-")}-"]`);
				if (label) label.htmlFor = field.id;
			});
			block.querySelector("[data-remove-system]").disabled = blocks.length === 1;
		});
		countLabel.textContent = blocks.length;
		addButton.disabled = blocks.length >= 10;
	};

	const appendBlock = () => {
		systemsContainer.appendChild(template.content.cloneNode(true));
		updateBlocks();
	};

	const validateSystems = () => {
		let isValid = true;
		const blocks = [...systemsContainer.querySelectorAll("[data-system-block]")];
		blocks.forEach((block) => {
			block.querySelectorAll("[data-field]").forEach((field) => {
				const valid = field.value.trim().length > 0;
				field.classList.toggle("is-invalid", !valid);
				if (!valid) isValid = false;
			});
		});
		if (!isValid) showAlert("Complete all required fields before running the pipeline.");
		else clearAlert();
		return isValid;
	};

	const collectSystems = () => [...systemsContainer.querySelectorAll("[data-system-block]")].map((block) => {
		const system = {};
		block.querySelectorAll("[data-field]").forEach((field) => { system[field.dataset.field] = field.value; });
		system.mode = selection.confirmed().configuration;
		return system;
	});
	let lastSystems = null;

	const formatMetric = (value) => typeof value === "number" ? value.toFixed(4) : "-";
	const renderRows = (items, target, columns) => {
		target.innerHTML = "";
		if (!items || items.length === 0) {
			target.innerHTML = `<tr><td colspan="${columns}" class="empty-state">No results available.</td></tr>`;
			return;
		}
		items.forEach((item) => {
			const row = document.createElement("tr");
			row.innerHTML = `<td>${item.system || "-"}</td><td>${item.proposal || "-"}</td><td>${formatMetric(item.precision)}</td><td>${formatMetric(item.recall)}</td><td>${formatMetric(item.f1_score)}</td>`;
			target.appendChild(row);
		});
	};

	const renderResults = (payload) => {
		const resultsAlert = document.querySelector("#results-alert");
		const messages = [...(payload.errors || []), ...(payload.warnings || [])].map((item) => `${item.system}: ${item.message}`);
		resultsAlert.className = messages.length ? "alert alert-warning" : "alert d-none";
		resultsAlert.textContent = messages.join(" ");
		if (payload.configuration || payload.ai_label) {
			const configuration = payload.configuration_label || (payload.configuration || "not recorded").toUpperCase();
			runSettingsSummary.textContent = `Run configuration: ${configuration} | AI: ${payload.ai_label || "not recorded"}`;
			runSettingsSummary.classList.remove("d-none");
		} else {
			runSettingsSummary.classList.add("d-none");
		}
		renderRows(payload.service_metrics, document.querySelector("#services-table-body"), 5);
		renderRows(payload.interaction_metrics, document.querySelector("#interactions-table-body"), 5);
		const bestBody = document.querySelector("#best-results-table-body");
		bestBody.innerHTML = "";
		if (!payload.best_results || payload.best_results.length === 0) {
			bestBody.innerHTML = '<tr><td colspan="3" class="empty-state">No best results available.</td></tr>';
		} else {
			payload.best_results.forEach((item) => {
				const row = document.createElement("tr");
				row.innerHTML = `<td>${item.system || "-"}</td><td>${item.best_services || "-"}</td><td>${item.best_interactions || "-"}</td>`;
				bestBody.appendChild(row);
			});
		}
		inputView.classList.add("d-none");
		resultsView.classList.remove("d-none");
		window.scrollTo({ top: 0, behavior: "smooth" });
	};

	const downloadPdf = async (url, filename) => {
		try {
			const response = await fetch(url, { cache: "no-store" });
			if (!response.ok) {
				let message = "The PDF could not be generated.";
				try {
					const errorPayload = await response.json();
					message = errorPayload.message || message;
				} catch (error) {
					// Keep the generic message when the server does not return JSON.
				}
				throw new Error(message);
			}
			const contentType = response.headers.get("Content-Type") || "";
			if (!contentType.includes("application/pdf")) throw new Error("The server returned an invalid PDF response.");
			const blobUrl = URL.createObjectURL(await response.blob());
			const link = document.createElement("a");
			link.href = blobUrl;
			link.download = filename;
			document.body.appendChild(link);
			link.click();
			link.remove();
			setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
		} catch (error) {
			showAlert(error.message || "The PDF could not be downloaded.");
		}
	};

	// --------------------------------------------------------------- progress
	const progressAnimation = {
		timer: null,
		displayed: 0,
		checkpoint: 0,
		boostUntil: 0,
		total: 1,
	};
	const MAX_VISIBLE_PERCENT = 99.4;

	const paintProgress = (percent, allowComplete = false) => {
		const ceiling = allowComplete ? 100 : MAX_VISIBLE_PERCENT;
		const rounded = Math.min(ceiling, Math.max(0, percent));
		progressBar.style.width = `${rounded.toFixed(2)}%`;
		progressPercent.textContent = `${Math.round(rounded)}%`;
		progressBar.parentElement.setAttribute("aria-valuenow", String(Math.round(rounded)));
	};

	const startProgressAnimation = (total) => {
		stopProgressAnimation();
		progressAnimation.displayed = 0;
		progressAnimation.checkpoint = 0;
		progressAnimation.boostUntil = 0;
		progressAnimation.total = Math.max(1, total);
		paintProgress(0);
		progressAnimation.timer = setInterval(() => {
			const step = 100 / progressAnimation.total;
			const ceiling = Math.min(99, progressAnimation.checkpoint + step * 0.7);
			const accelerated = Date.now() < progressAnimation.boostUntil;
			const rate = accelerated ? 0.16 : 0.022;
			if (progressAnimation.displayed < ceiling) {
				progressAnimation.displayed += (ceiling - progressAnimation.displayed) * rate;
			} else {
				progressAnimation.displayed = ceiling;
			}
			paintProgress(progressAnimation.displayed);
		}, 120);
	};

	function stopProgressAnimation() {
		if (progressAnimation.timer) {
			clearInterval(progressAnimation.timer);
			progressAnimation.timer = null;
		}
	}

	const updateProgress = (progress) => {
		const percent = Math.max(0, Math.min(100, Number(progress.percent) || 0));
		if (percent > progressAnimation.checkpoint) {
			progressAnimation.checkpoint = percent;
			progressAnimation.boostUntil = Date.now() + 2400;
		}
		progressStatus.textContent = progress.completed < progress.total
			? `Completed ${progress.completed} of ${progress.total} systems${progress.current_system ? ` | Running: ${progress.current_system}` : ""}`
			: "All systems processed. Preparing results...";
	};

	const watchProgress = (total) => {
		updateProgress({ percent: 0, completed: 0, total });
		return setInterval(async () => {
			try {
				const response = await fetch("/api/pipeline/progress", { cache: "no-store" });
				if (response.ok) updateProgress(await response.json());
			} catch (error) {
				// The run request remains the source of truth if a progress poll fails.
			}
		}, 500);
	};

	// -------------------------------------------------------------------- run
	const setSetupDisabled = (disabled) => {
		configurationToggle.disabled = disabled;
		providerToggle.disabled = disabled;
		saveKeyButton.disabled = disabled;
		newApiKeyInput.disabled = disabled;
		setActiveKeyCheckbox.disabled = disabled;
	};

	const executePipeline = async (systems) => {
		const confirmed = selection.confirmed();
		const provider = providerEntry(confirmed.provider);
		if (settingsPayload && (!provider || !provider.configured)) {
			showAlert(`Add an API key for ${provider ? provider.label : confirmed.provider} before running the pipeline.`, "warning");
			return;
		}
		// RUN AGAIN reuses the collected inputs but not the configuration of the
		// previous run: the mode active at this click is applied here.
		const runSystems = systems.map((system) => ({ ...system, mode: confirmed.configuration }));
		lastSystems = runSystems;
		runButton.disabled = true;
		rerunExperimentButton.disabled = true;
		rerunExperimentButton.textContent = "RUNNING PIPELINE...";
		runButton.textContent = "RUNNING PIPELINE...";
		setSetupDisabled(true);
		loadingAlert.classList.remove("d-none");
		const totalSystems = runSystems.length;
		startProgressAnimation(totalSystems);
		const progressWatcher = watchProgress(totalSystems);
		showAlert("The pipeline is running. This may take a few minutes. Please wait...", "info");
		const body = { systems: runSystems };
		if (settingsPayload) body.provider = confirmed.provider;
		let succeeded = false;
		try {
			const response = await fetch("/api/pipeline/run", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				cache: "no-store",
				body: JSON.stringify(body),
			});
			const payload = await response.json();
			if (!response.ok || !payload.ok) throw new Error(payload.message || "The pipeline run failed.");
			renderResults(payload);
			succeeded = true;
		} catch (error) {
			showAlert(error.message || "The pipeline run could not be completed.");
		} finally {
			clearInterval(progressWatcher);
			stopProgressAnimation();
			setSetupDisabled(false);
			if (succeeded) {
				paintProgress(100, true);
				setTimeout(() => loadingAlert.classList.add("d-none"), 450);
			} else {
				loadingAlert.classList.add("d-none");
			}
			runButton.disabled = false;
			rerunExperimentButton.disabled = false;
			rerunExperimentButton.textContent = "RUN AGAIN";
			runButton.textContent = "RUN PIPELINE";
		}
	};

	// ----------------------------------------------------------------- events
	configurationToggle.addEventListener("click", () => {
		if (openMenu === "configuration") requestConfirmation();
		else setMenu("configuration");
	});

	providerToggle.addEventListener("click", () => {
		if (openMenu === "provider") requestConfirmation();
		else setMenu("provider");
	});

	document.addEventListener("click", (event) => {
		if (!openMenu) return;
		// Selecting an option re-renders its menu, so the clicked element is
		// already detached when the event reaches the document. The composed
		// path still holds the original setup-group ancestor.
		const insideSetup = event.composedPath().some(
			(node) => node instanceof Element && node.matches("[data-setup-group]"),
		);
		if (insideSetup) return;
		if (!confirmBackdrop.classList.contains("d-none")) return;
		requestConfirmation();
	});

	document.addEventListener("keydown", (event) => {
		if (event.key === "Escape" && !confirmBackdrop.classList.contains("d-none")) discardConfirmation();
	});

	confirmAccept.addEventListener("click", acceptConfirmation);
	confirmDiscard.addEventListener("click", discardConfirmation);
	saveKeyButton.addEventListener("click", saveKey);
	newApiKeyInput.addEventListener("keydown", (event) => {
		if (event.key === "Enter") {
			event.preventDefault();
			saveKey();
		}
	});

	addButton.addEventListener("click", async () => {
		const currentCount = systemsContainer.querySelectorAll("[data-system-block]").length;
		if (currentCount >= 10) return;
		const response = await fetch("/api/systems", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ current_count: currentCount }),
		});
		if (!response.ok) return;
		appendBlock();
	});

	systemsContainer.addEventListener("click", async (event) => {
		const removeButton = event.target.closest("[data-remove-system]");
		if (!removeButton) return;
		const blocks = [...systemsContainer.querySelectorAll("[data-system-block]")];
		if (blocks.length === 1) return;
		const block = removeButton.closest("[data-system-block]");
		const index = blocks.indexOf(block);
		const response = await fetch(`/api/systems/${index}`, {
			method: "DELETE",
			headers: { "X-System-Count": String(blocks.length) },
		});
		if (!response.ok) return;
		block.remove();
		updateBlocks();
	});

	systemsContainer.addEventListener("input", (event) => {
		const field = event.target.closest("[data-field]");
		if (!field || field.value.trim().length === 0) return;
		field.classList.remove("is-invalid");
	});

	const startRun = async (reuse) => {
		if (!confirmBackdrop.classList.contains("d-none")) return;
		if (selection.isDirty()) {
			requestConfirmation(reuse ? () => executePipeline(lastSystems) : () => startRun(false));
			return;
		}
		if (reuse) {
			if (!lastSystems) return;
			await executePipeline(lastSystems);
			return;
		}
		if (!validateSystems()) return;
		lastSystems = collectSystems();
		await executePipeline(lastSystems);
	};

	runButton.addEventListener("click", () => startRun(false));
	rerunExperimentButton.addEventListener("click", () => startRun(true));

	newDecompositionButton.addEventListener("click", () => {
		document.querySelector("#decomposition-form").reset();
		systemsContainer.innerHTML = "";
		appendBlock();
		resultsView.classList.add("d-none");
		inputView.classList.remove("d-none");
		lastSystems = null;
		runSettingsSummary.classList.add("d-none");
		clearAlert();
		window.scrollTo({ top: 0, behavior: "smooth" });
	});

	if (downloadReportButton) {
		downloadReportButton.addEventListener("click", () => {
			downloadPdf("/api/report/pdf", "davinci-architecture-report.pdf");
		});
	}

	if (downloadSpecificationButton) {
		downloadSpecificationButton.addEventListener("click", () => {
			downloadPdf("/api/report/specification-pdf", "davinci-architectural-specification.pdf");
		});
	}

	appendBlock();
	loadSettings().then(renderSetup);
});
