/**
 * LLM Council Dashboard — Client-Side Application
 *
 * Vanilla JavaScript module that drives the council dashboard UI.
 * Communicates with the Python backend via REST and SSE-over-POST.
 *
 * No external dependencies.
 */

(function () {
  'use strict';

  // ---------------------------------------------------------------------------
  // Constants
  // ---------------------------------------------------------------------------

  const API = {
    MODELS: '/api/models',
    COUNCIL: '/api/council',
    COUNCIL_STREAM: '/api/council/stream',
    SYNTHESIZE: '/api/council/synthesize',
    VOTE: '/api/council/vote',
    CHAIRMAN: '/api/council/chairman',
  };

  const STORAGE_KEYS = {
    THEME: 'llm-council-theme',
    HISTORY: 'llm-council-history',
  };

  const MAX_HISTORY = 10;
  const MIN_MODELS = 2;

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------

  const state = {
    models: [],
    selectedModels: new Set(),
    responses: new Map(),
    isConvening: false,
    currentPrompt: '',
    dropdownOpen: false,
    chairmanModel: '',
    voteResults: null,
  };

  // ---------------------------------------------------------------------------
  // DOM References
  // ---------------------------------------------------------------------------

  const dom = {};

  function cacheDom() {
    dom.modelChipsContainer = document.getElementById('model-chips-container');
    dom.promptInput = document.getElementById('prompt-input');
    dom.systemPromptInput = document.getElementById('system-prompt-input');
    dom.systemPromptToggle = document.getElementById('system-prompt-toggle');
    dom.conveneBtn = document.getElementById('convene-btn');
    dom.responseGrid = document.getElementById('response-grid');
    dom.synthesisPanel = document.getElementById('synthesis-panel');
    dom.synthesisContent = document.getElementById('synthesis-content');
    dom.synthesizeBtn = document.getElementById('synthesize-btn');
    dom.historySidebar = document.getElementById('history-sidebar');
    dom.historyList = document.getElementById('history-list');
    dom.themeToggle = document.getElementById('theme-toggle');
    dom.statusIndicator = document.getElementById('status-indicator');
    dom.selectedCount = document.getElementById('selected-count');
    dom.votingPanel = document.getElementById('voting-panel');
    dom.startVoteBtn = document.getElementById('start-vote-btn');
    dom.votingCardsContainer = document.getElementById('voting-cards-container');
    dom.votingResults = document.getElementById('voting-results');
    dom.votingDescription = document.getElementById('voting-description');
    dom.triggerLabel = document.getElementById('trigger-label');
    dom.selectorTrigger = document.getElementById('model-selector-trigger');
    dom.modelDropdown = document.getElementById('model-dropdown');
    dom.selectAllBtn = document.getElementById('select-all-btn');
    dom.deselectAllBtn = document.getElementById('deselect-all-btn');
    dom.selectedTags = document.getElementById('selected-tags');
    dom.chairmanPanel = document.getElementById('chairman-panel');
    dom.chairmanModelSelect = document.getElementById('chairman-model-select');
    dom.startChairmanBtn = document.getElementById('start-chairman-btn');
    dom.chairmanContent = document.getElementById('chairman-content');
    dom.chairmanDescription = document.getElementById('chairman-description');
  }

  // ---------------------------------------------------------------------------
  // Initialization
  // ---------------------------------------------------------------------------

  document.addEventListener('DOMContentLoaded', async () => {
    cacheDom();
    loadTheme();
    renderHistory();
    wireEventListeners();
    await fetchModels();
  });

  // ---------------------------------------------------------------------------
  // API — Fetch Models
  // ---------------------------------------------------------------------------

  async function fetchModels() {
    setStatus('Loading models...');
    try {
      const res = await fetch(API.MODELS);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      state.models = data.models || [];
      renderModelChips();
      setStatus('Ready');
    } catch (err) {
      console.error('Failed to fetch models:', err);
      setStatus('Error loading models');
    }
  }

  // ---------------------------------------------------------------------------
  // Model Selector Dropdown
  // ---------------------------------------------------------------------------

  // Dropdown open/close: Uses CSS classes only. No document listeners, no
  // event propagation tricks. Close-on-outside-click handled via a single
  // permanent mousedown listener on document (see wireEventListeners).

  function openDropdown() {
    state.dropdownOpen = true;
    dom.selectorTrigger && dom.selectorTrigger.classList.add('open');
    dom.modelDropdown && dom.modelDropdown.classList.add('open');
  }

  function closeDropdown() {
    state.dropdownOpen = false;
    dom.selectorTrigger && dom.selectorTrigger.classList.remove('open');
    dom.modelDropdown && dom.modelDropdown.classList.remove('open');
  }

  function renderModelChips() {
    if (!dom.modelChipsContainer) return;
    dom.modelChipsContainer.innerHTML = '';
    state.selectedModels.clear();

    state.models.forEach(function (model) {
      var li = document.createElement('li');
      li.className = 'model-option selected';
      li.dataset.modelId = model.id;
      li.dataset.provider = model.provider;

      var providerClass = 'provider-' + model.provider.toLowerCase().replace(/[^a-z0-9]/g, '');

      li.innerHTML =
        '<span class="option-checkbox">&#10003;</span>' +
        '<span class="option-info">' +
          '<span class="option-name">' + escapeHtml(model.name) + '</span>' +
          '<span class="option-id">' + escapeHtml(model.id) + '</span>' +
        '</span>' +
        '<span class="provider-badge ' + providerClass + '">' + escapeHtml(model.provider) + '</span>';

      li.addEventListener('click', function (e) {
        e.stopPropagation();
        toggleModelOption(li, model.id);
      });

      dom.modelChipsContainer.appendChild(li);
      state.selectedModels.add(model.id);
    });

    updateSelectedCount();
    renderSelectedTags();
  }

  function toggleModelOption(optionEl, modelId) {
    if (optionEl.classList.contains('selected')) {
      optionEl.classList.remove('selected');
      state.selectedModels.delete(modelId);
    } else {
      optionEl.classList.add('selected');
      state.selectedModels.add(modelId);
    }
    updateSelectedCount();
    renderSelectedTags();
  }

  function selectAllModels(doSelect) {
    var options = dom.modelChipsContainer.querySelectorAll('.model-option');
    options.forEach(function (opt) {
      var id = opt.dataset.modelId;
      if (doSelect) {
        opt.classList.add('selected');
        state.selectedModels.add(id);
      } else {
        opt.classList.remove('selected');
        state.selectedModels.delete(id);
      }
    });
    updateSelectedCount();
    renderSelectedTags();
  }

  function updateSelectedCount() {
    var n = state.selectedModels.size;
    if (dom.selectedCount) {
      dom.selectedCount.textContent = n;
      dom.selectedCount.classList.toggle('zero', n === 0);
    }
    if (dom.triggerLabel) {
      dom.triggerLabel.textContent = n === 0 ? 'Select Models' : 'Models';
    }
  }

  function renderSelectedTags() {
    if (!dom.selectedTags) return;
    dom.selectedTags.innerHTML = '';

    var modelLookup = {};
    state.models.forEach(function (m) { modelLookup[m.id] = m; });

    state.selectedModels.forEach(function (id) {
      var model = modelLookup[id];
      if (!model) return;

      var tag = document.createElement('span');
      tag.className = 'selected-tag';
      tag.dataset.provider = model.provider;
      tag.innerHTML = escapeHtml(model.name) + ' <span class="tag-remove">&#10005;</span>';
      tag.title = 'Remove ' + model.name;
      tag.addEventListener('click', function () {
        state.selectedModels.delete(id);
        var opt = dom.modelChipsContainer.querySelector('[data-model-id="' + id.replace(/\//g, '\\/').replace(/\./g, '\\.') + '"]');
        if (opt) opt.classList.remove('selected');
        updateSelectedCount();
        renderSelectedTags();
      });
      dom.selectedTags.appendChild(tag);
    });
  }

  // ---------------------------------------------------------------------------
  // Theme Toggle
  // ---------------------------------------------------------------------------

  function loadTheme() {
    var saved = localStorage.getItem(STORAGE_KEYS.THEME) || 'dark';
    applyTheme(saved);
  }

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem(STORAGE_KEYS.THEME, theme);
    if (dom.themeToggle) {
      dom.themeToggle.textContent = theme === 'dark' ? '\u2600' : '\u263E';
    }
  }

  function toggleTheme() {
    var current = document.documentElement.dataset.theme || 'dark';
    applyTheme(current === 'dark' ? 'light' : 'dark');
  }

  // ---------------------------------------------------------------------------
  // System Prompt Toggle
  // ---------------------------------------------------------------------------

  function toggleSystemPrompt() {
    if (!dom.systemPromptInput) return;
    var wrapper = dom.systemPromptInput.closest('.system-prompt-wrapper');
    if (!wrapper) return;
    var isHidden = wrapper.classList.contains('collapsed');
    if (isHidden) {
      wrapper.classList.remove('collapsed');
      wrapper.classList.add('expanded');
    } else {
      wrapper.classList.remove('expanded');
      wrapper.classList.add('collapsed');
    }
  }

  // ---------------------------------------------------------------------------
  // Status Indicator
  // ---------------------------------------------------------------------------

  function setStatus(text) {
    if (dom.statusIndicator) dom.statusIndicator.textContent = text;
  }

  // ---------------------------------------------------------------------------
  // Convene Council — Main Action
  // ---------------------------------------------------------------------------

  async function conveneCouncil() {
    if (state.isConvening) return;

    var prompt = (dom.promptInput ? dom.promptInput.value.trim() : '');
    if (!prompt) {
      shakeElement(dom.promptInput);
      return;
    }
    if (state.selectedModels.size < MIN_MODELS) {
      setStatus('Select at least ' + MIN_MODELS + ' models');
      return;
    }

    state.isConvening = true;
    state.currentPrompt = prompt;
    state.responses.clear();
    setConveneEnabled(false);
    setSynthesizeEnabled(false);
    setStatus('Querying...');

    if (dom.responseGrid) dom.responseGrid.innerHTML = '';
    if (dom.synthesisContent) dom.synthesisContent.innerHTML = '';
    if (dom.synthesisPanel) dom.synthesisPanel.classList.remove('visible');
    if (dom.votingPanel) dom.votingPanel.classList.remove('visible');
    if (dom.chairmanPanel) dom.chairmanPanel.classList.remove('visible');
    state.voteResults = null;
    state.chairmanModel = '';

    var selectedIds = Array.from(state.selectedModels);
    var modelLookup = {};
    state.models.forEach(function (m) { modelLookup[m.id] = m; });

    selectedIds.forEach(function (id) {
      var info = modelLookup[id] || { id: id, name: id, provider: 'Unknown' };
      var card = createResponseCard(id, info.name, info.provider);
      if (dom.responseGrid) dom.responseGrid.appendChild(card);
      state.responses.set(id, { content: '', status: 'pending', duration: 0, tokenCount: 0 });
    });

    var body = { prompt: prompt, models: selectedIds };
    var systemPrompt = dom.systemPromptInput ? dom.systemPromptInput.value.trim() : '';
    if (systemPrompt) body.system_prompt = systemPrompt;

    try {
      await streamCouncilResponses(body);
    } catch (err) {
      console.error('Council streaming error:', err);
      setStatus('Error');
    }

    state.isConvening = false;
    setConveneEnabled(true);
    setStatus('Complete');

    var hasCompleted = Array.from(state.responses.values()).some(function (r) { return r.status === 'complete'; });
    setSynthesizeEnabled(hasCompleted);

    // Show voting panel if 2+ completed
    var completedCount = Array.from(state.responses.values()).filter(function (r) { return r.status === 'complete'; }).length;
    if (completedCount >= 2) {
      if (dom.votingPanel) dom.votingPanel.classList.add('visible');
      if (dom.startVoteBtn) {
        dom.startVoteBtn.disabled = false;
        dom.startVoteBtn.textContent = 'Run Anonymous Model Vote';
      }
      if (dom.votingCardsContainer) dom.votingCardsContainer.innerHTML = '';
      if (dom.votingResults) dom.votingResults.style.display = 'none';
      if (dom.votingDescription) {
        dom.votingDescription.textContent =
          'Each model anonymously evaluates every other model\'s response and votes for the best one.';
      }
    }

    saveToHistory(prompt, selectedIds);
  }

  // ---------------------------------------------------------------------------
  // SSE-over-POST Streaming
  // ---------------------------------------------------------------------------

  async function streamCouncilResponses(body) {
    var response = await fetch(API.COUNCIL_STREAM, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error('HTTP ' + response.status);

    var reader = response.body.getReader();
    var decoder = new TextDecoder('utf-8');
    var buffer = '';
    var streamDone = false;

    function processLine(line) {
      line = line.trim();
      if (!line || line.startsWith(':')) return;
      if (line.startsWith('data:')) {
        var jsonStr = line.slice(5).trim();
        if (!jsonStr) return;
        try {
          var parsed = JSON.parse(jsonStr);
          if (parsed.status === 'done') {
            streamDone = true;
            return;
          }
          handleSSEEvent(parsed);
        } catch (_) { /* skip malformed JSON */ }
      }
    }

    while (true) {
      var chunk = await reader.read();
      if (chunk.done) break;
      buffer += decoder.decode(chunk.value, { stream: true });

      var endsWithNewline = buffer.endsWith('\n');
      var segments = buffer.split('\n');
      buffer = endsWithNewline ? '' : segments.pop();

      for (var i = 0; i < segments.length; i++) {
        processLine(segments[i]);
      }

      // Break out of read loop as soon as server signals done,
      // rather than waiting for the proxy to close the connection
      if (streamDone) break;
    }

    // Process any remaining data in the buffer
    if (buffer.trim()) {
      processLine(buffer);
    }

    // Cancel the reader if stream is done but connection still open
    if (streamDone) {
      try { reader.cancel(); } catch (_) {}
    }
  }

  function handleSSEEvent(event) {
    var modelId = event.model;
    if (!modelId) return;

    var cardEl = dom.responseGrid
      ? dom.responseGrid.querySelector('.response-card[data-model="' + CSS.escape(modelId) + '"]')
      : null;
    if (!cardEl) return;

    var contentEl = cardEl.querySelector('.card-content');
    var statusEl = cardEl.querySelector('.card-status');
    var tokenCountEl = cardEl.querySelector('.token-count');
    var durationEl = cardEl.querySelector('.duration');

    var rs = state.responses.get(modelId) || { content: '', status: 'pending', duration: 0, tokenCount: 0 };

    if (event.status === 'started') {
      rs.status = 'streaming';
      if (statusEl) statusEl.innerHTML = '<span class="spinner"></span>';
      if (contentEl) contentEl.innerHTML = '<div class="typing-indicator">Generating...</div>';
      cardEl.classList.add('streaming');
      cardEl.classList.remove('loading');
    } else if (event.status === 'streaming') {
      rs.content = event.content || rs.content;
      rs.status = 'streaming';
      if (contentEl) { contentEl.innerHTML = renderMarkdown(rs.content); scrollToBottom(contentEl); }
      if (statusEl) statusEl.innerHTML = '<span class="spinner"></span>';
      cardEl.classList.add('streaming');
      cardEl.classList.remove('loading');
    } else if (event.status === 'complete') {
      rs.content = event.content || rs.content;
      rs.status = 'complete';
      rs.duration = event.duration || 0;
      rs.tokenCount = event.token_count || 0;
      if (contentEl) contentEl.innerHTML = renderMarkdown(rs.content);
      if (statusEl) statusEl.innerHTML = '<span class="check-icon">&#10003;</span>';
      if (tokenCountEl) tokenCountEl.textContent = rs.tokenCount + ' tokens';
      if (durationEl) durationEl.textContent = rs.duration.toFixed(2) + 's';
      cardEl.classList.remove('streaming', 'loading');
      cardEl.classList.add('complete');
    } else if (event.status === 'error') {
      rs.content = event.content || 'An error occurred.';
      rs.status = 'error';
      if (contentEl) contentEl.innerHTML = '<p class="error-message">' + escapeHtml(rs.content) + '</p>';
      if (statusEl) statusEl.innerHTML = '<span class="error-icon">&#10007;</span>';
      cardEl.classList.remove('streaming', 'loading');
      cardEl.classList.add('error');
    }

    state.responses.set(modelId, rs);

    // Update status indicator
    var completed = 0;
    var total = 0;
    state.responses.forEach(function (r) {
      total++;
      if (r.status === 'complete' || r.status === 'error') completed++;
    });
    if (completed < total) {
      setStatus('Querying... (' + completed + '/' + total + ')');
    } else {
      setStatus('Complete');
    }
  }

  // ---------------------------------------------------------------------------
  // Response Card
  // ---------------------------------------------------------------------------

  function createResponseCard(modelId, modelName, provider) {
    var card = document.createElement('div');
    card.className = 'response-card loading';
    card.dataset.model = modelId;
    card.dataset.provider = provider;
    var providerClass = 'provider-' + provider.toLowerCase().replace(/[^a-z0-9]/g, '');

    card.innerHTML =
      '<div class="card-header">' +
        '<span class="model-name">' + escapeHtml(modelName) + '</span>' +
        '<span class="provider-badge ' + providerClass + '">' + escapeHtml(provider) + '</span>' +
        '<span class="card-status"><span class="spinner"></span></span>' +
      '</div>' +
      '<div class="card-content"><div class="typing-indicator">...</div></div>' +
      '<div class="card-footer">' +
        '<span class="token-count"></span><span class="duration"></span>' +
        '<button class="copy-btn" title="Copy response">Copy</button>' +
      '</div>';

    card.querySelector('.copy-btn').addEventListener('click', function () {
      handleCopy(modelId, card.querySelector('.copy-btn'));
    });
    return card;
  }

  // ---------------------------------------------------------------------------
  // Copy
  // ---------------------------------------------------------------------------

  async function handleCopy(modelId, btnEl) {
    var rd = state.responses.get(modelId);
    if (!rd || !rd.content) return;
    try {
      await navigator.clipboard.writeText(rd.content);
    } catch (_) {
      var ta = document.createElement('textarea');
      ta.value = rd.content; ta.style.cssText = 'position:fixed;opacity:0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); } catch (__) { /* */ }
      document.body.removeChild(ta);
    }
    btnEl.textContent = 'Copied!'; btnEl.classList.add('copied');
    setTimeout(function () { btnEl.textContent = 'Copy'; btnEl.classList.remove('copied'); }, 1500);
  }

  // ---------------------------------------------------------------------------
  // Synthesis
  // ---------------------------------------------------------------------------

  async function synthesizeResponses() {
    if (!dom.synthesisPanel || !dom.synthesisContent) return;
    var completed = [];
    state.responses.forEach(function (data, modelId) {
      if (data.status === 'complete') completed.push({ model: modelId, content: data.content });
    });
    if (completed.length < MIN_MODELS) { setStatus('Need ' + MIN_MODELS + '+ responses'); return; }

    dom.synthesisPanel.classList.add('visible');
    dom.synthesisContent.innerHTML = '<div class="typing-indicator">Synthesizing...</div>';
    setSynthesizeEnabled(false);
    setStatus('Synthesizing...');

    try {
      var res = await fetch(API.SYNTHESIZE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: state.currentPrompt, responses: completed }),
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      var data = await res.json();
      dom.synthesisContent.innerHTML = renderMarkdown(data.synthesis || 'No synthesis.');
      setStatus('Complete');
    } catch (err) {
      dom.synthesisContent.innerHTML = '<p class="error-message">Synthesis failed: ' + escapeHtml(err.message) + '</p>';
      setStatus('Synthesis error');
    }
    setSynthesizeEnabled(true);
  }

  // ---------------------------------------------------------------------------
  // Anonymous Model Voting (Models vote on each other)
  // ---------------------------------------------------------------------------

  async function runAnonymousModelVote() {
    var completed = [];
    state.responses.forEach(function (data, modelId) {
      if (data.status === 'complete' && data.content) {
        completed.push({ modelId: modelId, content: data.content });
      }
    });

    if (completed.length < 2) {
      setStatus('Need 2+ completed responses to vote');
      return;
    }

    if (dom.startVoteBtn) dom.startVoteBtn.disabled = true;
    if (dom.votingCardsContainer) dom.votingCardsContainer.innerHTML = '';
    if (dom.votingResults) dom.votingResults.style.display = 'none';
    if (dom.votingDescription) {
      dom.votingDescription.textContent =
        'Asking each model to anonymously judge all other responses... This may take a moment.';
    }
    setStatus('Models voting...');

    // Show a progress card for each voter
    var modelLookup = {};
    state.models.forEach(function (m) { modelLookup[m.id] = m; });

    completed.forEach(function (entry) {
      var info = modelLookup[entry.modelId] || { name: entry.modelId, provider: 'Unknown' };
      var el = document.createElement('div');
      el.className = 'vote-card';
      el.dataset.voter = entry.modelId;
      el.innerHTML =
        '<div class="vote-card-label">' +
          '<span>Voter: ' + escapeHtml(info.name) + '</span>' +
          '<span class="vote-badge"><span class="spinner" style="width:12px;height:12px;border-width:1.5px"></span> Judging...</span>' +
        '</div>';
      if (dom.votingCardsContainer) dom.votingCardsContainer.appendChild(el);
    });

    // Call backend to run the vote (SSE stream with keepalive pings)
    try {
      var res = await fetch(API.VOTE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: state.currentPrompt,
          responses: completed.map(function (c) { return { model: c.modelId, content: c.content }; }),
        }),
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);

      // Read SSE stream — server sends keepalive pings and a final data event
      var reader = res.body.getReader();
      var decoder = new TextDecoder('utf-8');
      var buf = '';
      var voteResult = null;

      while (true) {
        var chunk = await reader.read();
        if (chunk.done) break;
        buf += decoder.decode(chunk.value, { stream: true });

        var endsNl = buf.endsWith('\n');
        var segs = buf.split('\n');
        buf = endsNl ? '' : segs.pop();

        for (var si = 0; si < segs.length; si++) {
          var ln = segs[si].trim();
          if (!ln || ln.startsWith(':')) continue; // keepalive or empty
          if (ln.startsWith('data:')) {
            try {
              var parsed = JSON.parse(ln.slice(5).trim());
              if (parsed.status === 'done' && parsed.result) {
                voteResult = parsed.result;
              } else if (parsed.status === 'error') {
                throw new Error(parsed.error || 'Vote failed');
              }
            } catch (pe) {
              if (pe.message && pe.message !== 'Vote failed' && !pe.message.startsWith('Vote')) {
                // JSON parse error, skip
              } else {
                throw pe;
              }
            }
          }
        }
        if (voteResult) {
          try { reader.cancel(); } catch (_) {}
          break;
        }
      }

      if (voteResult) {
        displayVoteResults(voteResult, completed, modelLookup);
      } else {
        throw new Error('No vote result received');
      }
    } catch (err) {
      if (dom.votingDescription) {
        dom.votingDescription.textContent = 'Voting failed: ' + err.message;
      }
      setStatus('Vote error');
    }

    if (dom.startVoteBtn) {
      dom.startVoteBtn.disabled = false;
      dom.startVoteBtn.textContent = 'Run Again';
    }
  }

  function displayVoteResults(data, completed, modelLookup) {
    // Save vote results for chairman
    state.voteResults = data;
    // data = { votes: { modelId: { score: N, voters: [...] } }, winner: modelId, details: [...] }
    if (dom.votingCardsContainer) dom.votingCardsContainer.innerHTML = '';
    if (dom.votingDescription) {
      dom.votingDescription.textContent = 'Each model anonymously scored the other responses. Results:';
    }

    var votes = data.votes || {};
    var details = data.details || [];
    var winner = data.winner || '';

    // Sort by score descending
    var sorted = Object.keys(votes).sort(function (a, b) {
      return (votes[b].score || 0) - (votes[a].score || 0);
    });

    var maxScore = sorted.length > 0 ? (votes[sorted[0]].score || 0) : 1;

    // Show result cards
    sorted.forEach(function (modelId, idx) {
      var info = modelLookup[modelId] || { name: modelId, provider: 'Unknown' };
      var v = votes[modelId];
      var isWinner = modelId === winner;
      var card = document.createElement('div');
      card.className = 'vote-card revealed' + (isWinner ? ' winner' : '');

      var rankLabel = '#' + (idx + 1);
      var providerClass = 'provider-' + (info.provider || 'unknown').toLowerCase().replace(/[^a-z]/g, '');

      card.innerHTML =
        '<div class="vote-card-label">' +
          '<span>' + rankLabel + ' ' + escapeHtml(info.name) + ' <span class="provider-badge ' + providerClass + '" style="margin-left:6px">' + escapeHtml(info.provider || '') + '</span></span>' +
          '<span class="vote-badge" style="' + (isWinner ? 'background:var(--color-success);color:#fff' : '') + '">' +
            (v.score || 0) + ' pts' + (isWinner ? ' -- Winner' : '') +
          '</span>' +
        '</div>' +
        '<div class="vote-card-content">' +
          '<div style="margin-bottom:8px">' +
            '<strong>Votes received from:</strong>' +
          '</div>' +
          (v.voters || []).map(function (voter) {
            var voterInfo = modelLookup[voter.voter] || { name: voter.voter };
            return '<div style="padding:4px 0;border-bottom:1px solid var(--color-border);font-size:0.82rem">' +
              '<span style="font-weight:600">' + escapeHtml(voterInfo.name) + '</span>: ' +
              '<span style="color:var(--color-coral);font-weight:700">+' + (voter.points || 0) + '</span>' +
              (voter.reason ? ' -- <span style="color:var(--color-text-secondary);font-style:italic">' + escapeHtml(voter.reason) + '</span>' : '') +
            '</div>';
          }).join('') +
        '</div>';

      if (dom.votingCardsContainer) dom.votingCardsContainer.appendChild(card);
    });

    // Summary bar chart
    if (dom.votingResults && sorted.length > 0) {
      dom.votingResults.style.display = 'block';
      var html = '<div class="results-title">Score Summary</div>';
      sorted.forEach(function (modelId, idx) {
        var info = modelLookup[modelId] || { name: modelId, provider: 'Unknown' };
        var v = votes[modelId];
        var score = v.score || 0;
        var pct = maxScore > 0 ? Math.round((score / maxScore) * 100) : 0;
        var rankClass = idx === 0 ? 'gold' : (idx === 1 ? 'silver' : '');
        var providerKey = (info.provider || '').toLowerCase().replace(/[^a-z]/g, '');
        var barClass = 'bar-' + (providerKey || 'default');

        html += '<div class="result-row">' +
          '<span class="result-rank ' + rankClass + '">#' + (idx + 1) + '</span>' +
          '<span class="result-model">' + escapeHtml(info.name) + '</span>' +
          '<div class="result-bar-container"><div class="result-bar ' + barClass + '" style="width:' + pct + '%"></div></div>' +
          '<span class="result-votes">' + score + ' pts</span>' +
          '</div>';
      });
      dom.votingResults.innerHTML = html;
    }

    setStatus('Vote complete');

    // Show chairman panel after voting completes
    if (dom.chairmanPanel) {
      dom.chairmanPanel.classList.add('visible');
      populateChairmanSelector();
      if (dom.startChairmanBtn) {
        dom.startChairmanBtn.disabled = false;
        dom.startChairmanBtn.textContent = 'Request Chairman Review';
      }
      if (dom.chairmanContent) dom.chairmanContent.innerHTML = '';
    }
  }

  // ---------------------------------------------------------------------------
  // Chairman
  // ---------------------------------------------------------------------------

  function populateChairmanSelector() {
    if (!dom.chairmanModelSelect) return;
    dom.chairmanModelSelect.innerHTML = '<option value="">Select chairman...</option>';
    state.selectedModels.forEach(function (modelId) {
      var model = state.models.find(function (m) { return m.id === modelId; });
      if (!model) return;
      var opt = document.createElement('option');
      opt.value = modelId;
      opt.textContent = model.name;
      dom.chairmanModelSelect.appendChild(opt);
    });
  }

  async function runChairmanReview() {
    if (!state.chairmanModel) {
      if (dom.chairmanDescription) {
        dom.chairmanDescription.textContent = 'Please select a chairman model first.';
        dom.chairmanDescription.style.color = 'var(--color-error)';
      }
      return;
    }
    if (!state.voteResults) {
      setStatus('Must run voting first');
      return;
    }

    var completed = [];
    state.responses.forEach(function (data, modelId) {
      if (data.status === 'complete' && data.content) {
        completed.push({ model: modelId, content: data.content, status: 'complete' });
      }
    });
    if (completed.length < 2) {
      setStatus('Need 2+ completed responses');
      return;
    }

    if (dom.chairmanDescription) {
      dom.chairmanDescription.style.color = 'var(--color-text-muted)';
      dom.chairmanDescription.textContent = 'Chairman is reviewing all responses and voting results...';
    }
    if (dom.startChairmanBtn) dom.startChairmanBtn.disabled = true;
    if (dom.chairmanModelSelect) dom.chairmanModelSelect.disabled = true;
    if (dom.chairmanContent) {
      dom.chairmanContent.style.display = 'block';
      dom.chairmanContent.innerHTML = '<div class="typing-indicator">Chairman is deliberating...</div>';
    }
    setStatus('Chairman reviewing...');

    try {
      var res = await fetch(API.CHAIRMAN, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: state.currentPrompt,
          responses: completed,
          vote_results: state.voteResults,
          chairman_model: state.chairmanModel,
        }),
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);

      // Read SSE stream with keepalive pings
      var reader = res.body.getReader();
      var decoder = new TextDecoder('utf-8');
      var buf = '';
      var chairmanResult = null;

      while (true) {
        var chunk = await reader.read();
        if (chunk.done) break;
        buf += decoder.decode(chunk.value, { stream: true });

        var endsNl = buf.endsWith('\n');
        var segs = buf.split('\n');
        buf = endsNl ? '' : segs.pop();

        for (var si = 0; si < segs.length; si++) {
          var ln = segs[si].trim();
          if (!ln || ln.startsWith(':')) continue;
          if (ln.startsWith('data:')) {
            try {
              var parsed = JSON.parse(ln.slice(5).trim());
              if (parsed.status === 'done' && parsed.result) {
                chairmanResult = parsed.result;
              } else if (parsed.status === 'error') {
                throw new Error(parsed.error || 'Chairman review failed');
              }
            } catch (pe) {
              if (pe.message && pe.message.indexOf('Chairman') === -1) {
                /* JSON parse error, skip */
              } else { throw pe; }
            }
          }
        }
        if (chairmanResult) {
          try { reader.cancel(); } catch (_) {}
          break;
        }
      }

      if (chairmanResult) {
        if (dom.chairmanContent) {
          dom.chairmanContent.innerHTML = renderMarkdown(chairmanResult);
        }
        var modelInfo = state.models.find(function (m) { return m.id === state.chairmanModel; });
        if (dom.chairmanDescription) {
          dom.chairmanDescription.textContent =
            'Final answer from ' + (modelInfo ? modelInfo.name : state.chairmanModel) + ' as chairman.';
        }
        setStatus('Chairman review complete');
      } else {
        throw new Error('No chairman result received');
      }
    } catch (err) {
      if (dom.chairmanContent) {
        dom.chairmanContent.innerHTML = '<p class="error-message">Chairman review failed: ' + escapeHtml(err.message) + '</p>';
      }
      if (dom.chairmanDescription) {
        dom.chairmanDescription.textContent = 'Chairman review failed: ' + err.message;
        dom.chairmanDescription.style.color = 'var(--color-error)';
      }
      setStatus('Chairman error');
    }

    if (dom.startChairmanBtn) {
      dom.startChairmanBtn.disabled = false;
      dom.startChairmanBtn.textContent = 'Request Again';
    }
    if (dom.chairmanModelSelect) dom.chairmanModelSelect.disabled = false;
  }

  // ---------------------------------------------------------------------------
  // History
  // ---------------------------------------------------------------------------

  function getHistory() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEYS.HISTORY)) || []; }
    catch (_) { return []; }
  }

  function saveToHistory(prompt, modelIds) {
    var history = getHistory();
    var summary = [];
    state.responses.forEach(function (data, modelId) {
      summary.push({ model: modelId, status: data.status, tokenCount: data.tokenCount, duration: data.duration, preview: (data.content || '').slice(0, 120) });
    });
    history.unshift({ timestamp: Date.now(), prompt: prompt, models: modelIds, responses: summary });
    while (history.length > MAX_HISTORY) history.pop();
    localStorage.setItem(STORAGE_KEYS.HISTORY, JSON.stringify(history));
    renderHistory();
  }

  function renderHistory() {
    if (!dom.historyList) return;
    var history = getHistory();
    if (history.length === 0) { dom.historyList.innerHTML = '<li class="history-empty">No history yet</li>'; return; }
    dom.historyList.innerHTML = '';
    history.forEach(function (entry) {
      var li = document.createElement('li');
      li.className = 'history-item';
      var date = new Date(entry.timestamp);
      var timeStr = date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) + ' ' + date.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
      var preview = entry.prompt.length > 60 ? entry.prompt.slice(0, 60) + '...' : entry.prompt;
      li.innerHTML = '<span class="history-time">' + escapeHtml(timeStr) + '</span><span class="history-prompt">' + escapeHtml(preview) + '</span><span class="history-meta">' + entry.models.length + ' models</span>';
      li.addEventListener('click', function () {
        if (dom.promptInput) dom.promptInput.value = entry.prompt;
      });
      dom.historyList.appendChild(li);
    });
  }

  // ---------------------------------------------------------------------------
  // Simple Markdown Renderer
  // ---------------------------------------------------------------------------

  function renderMarkdown(text) {
    if (!text) return '';
    var html = escapeHtml(text);
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, function (_, lang, code) {
      return '<pre class="code-block"><code>' + code + '</code></pre>';
    });
    html = html.replace(/`([^`\n]+)`/g, '<code class="inline-code">$1</code>');
    html = html.replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*([^\*]+)\*/g, '<em>$1</em>');
    html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    html = html.replace(/^---$/gm, '<hr>');
    html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
    html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>');
    html = html.replace(/\n{2,}/g, '</p><p>');
    html = '<p>' + html + '</p>';
    html = html.replace(/(<pre[\s\S]*?<\/pre>)|(\n)/g, function (m, pre) { return pre ? pre : '<br>'; });
    html = html.replace(/<p>\s*<\/p>/g, '');
    return html;
  }

  // ---------------------------------------------------------------------------
  // Event Listeners
  // ---------------------------------------------------------------------------

  function wireEventListeners() {
    if (dom.themeToggle) dom.themeToggle.addEventListener('click', toggleTheme);
    if (dom.systemPromptToggle) dom.systemPromptToggle.addEventListener('click', toggleSystemPrompt);
    if (dom.conveneBtn) dom.conveneBtn.addEventListener('click', conveneCouncil);
    if (dom.synthesizeBtn) dom.synthesizeBtn.addEventListener('click', synthesizeResponses);
    if (dom.startVoteBtn) dom.startVoteBtn.addEventListener('click', runAnonymousModelVote);
    if (dom.startChairmanBtn) dom.startChairmanBtn.addEventListener('click', runChairmanReview);
    if (dom.chairmanModelSelect) dom.chairmanModelSelect.addEventListener('change', function () {
      state.chairmanModel = dom.chairmanModelSelect.value;
    });

    // Dropdown trigger: simple click toggle
    if (dom.selectorTrigger) {
      dom.selectorTrigger.addEventListener('click', function (e) {
        e.stopPropagation();
        if (state.dropdownOpen) { closeDropdown(); } else { openDropdown(); }
      });
    }
    if (dom.selectAllBtn) dom.selectAllBtn.addEventListener('click', function (e) { e.stopPropagation(); selectAllModels(true); });
    if (dom.deselectAllBtn) dom.deselectAllBtn.addEventListener('click', function (e) { e.stopPropagation(); selectAllModels(false); });

    // Close dropdown when clicking ANYWHERE outside
    // Uses mousedown (fires before click) on document to close dropdown
    document.addEventListener('mousedown', function (e) {
      if (!state.dropdownOpen) return;
      // Check if click is inside the model-selector (trigger + dropdown)
      var selector = document.getElementById('model-selector');
      if (selector && selector.contains(e.target)) return;
      closeDropdown();
    });

    // Keyboard
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        conveneCouncil();
      }
      if (e.key === 'Escape') closeDropdown();
    });
  }

  // ---------------------------------------------------------------------------
  // UI Helpers
  // ---------------------------------------------------------------------------

  function setConveneEnabled(on) {
    if (!dom.conveneBtn) return;
    dom.conveneBtn.disabled = !on;
    dom.conveneBtn.classList.toggle('disabled', !on);
  }

  function setSynthesizeEnabled(on) {
    if (!dom.synthesizeBtn) return;
    dom.synthesizeBtn.disabled = !on;
    dom.synthesizeBtn.classList.toggle('disabled', !on);
  }

  function shakeElement(el) {
    if (!el) return;
    el.classList.add('shake');
    setTimeout(function () { el.classList.remove('shake'); }, 500);
  }

  function scrollToBottom(el) {
    if (el) el.scrollTop = el.scrollHeight;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

})();
