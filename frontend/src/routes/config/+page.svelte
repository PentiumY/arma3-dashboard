<script>
  import { onMount } from 'svelte';

  import Header from '$lib/components/Header.svelte';
  import { fly } from 'svelte/transition';
  import api from '$lib/api';

  let presets = [];
  let selectedPreset = '';
  let hostname = '';
  let presetName = '';
  let password = '';
  let adminPassword = '';
  let maxPlayers = 40;
  let persistent = false;
  let battleye = true;
  let verifySignatures = 2;
  let motd = '';
  let showModal = false;

  onMount(async () => {
    presets = await api.get('presets');
    
    selectedPreset = await api.get('current');

    console.log(selectedPreset)
    console.log(presets);

    loadPreset()
  });

  async function loadPreset() {
    presetName = selectedPreset

    const data = await api.get(`presets/${selectedPreset}`);

    hostname = data.hostname;
    password = data.password;
    adminPassword = data.passwordAdmin;
    maxPlayers = data.maxPlayers;
    persistent = data.persistent;
    battleye = data.battleye;
    verifySignatures = data.verifySignatures;
    motd = data.motd?.join("\n") ?? '';

    await api.post('setCurrent', { name: selectedPreset });
  }

  async function saveSettings() {
    await api.post('save', {
        name: presetName,
        data: {
            hostname,
            password,
            passwordAdmin: adminPassword,
            maxPlayers,
            persistent,
            battleye,
            verifySignatures,
            motd: motd.split("\n")
          }
        });

    showModal = true;
  }
  
</script>

<Header current="/config" />

<div class="min-h-screen bg-gray-100 p-6">
  <div class="max-w-4xl mx-auto bg-white shadow rounded-xl p-6 space-y-6">
    <h1 class="text-3xl font-bold mb-4">Arma 3 Server Dashboard</h1>

    <div class="grid grid-cols-1 gap-4">
      <div>
        <label class="font-semibold">Preset</label>
        <select bind:value={selectedPreset} on:change={loadPreset} class="mt-1 w-full border rounded p-2">
          <option value="">Select preset...</option>
          {#each presets as p}
            <option value={p}>{p}</option>
          {/each}
        </select>
      </div>

      <div>
        <label class="font-semibold">Hostname</label>
        <input bind:value={hostname} class="mt-1 w-full border rounded p-2" />
      </div>

      <div>
        <label class="font-semibold">Server Password</label>
        <input bind:value={password} class="mt-1 w-full border rounded p-2" />
      </div>

      <div>
        <label class="font-semibold">Admin Password</label>
        <input bind:value={adminPassword} class="mt-1 w-full border rounded p-2" />
      </div>

      <div>
        <label class="font-semibold">Max Players</label>
        <input type="number" bind:value={maxPlayers} class="mt-1 w-full border rounded p-2" />
      </div>

      <div class="flex items-center space-x-2">
        <input type="checkbox" bind:checked={persistent} />
        <label>Persistent Mission</label>
      </div>

      <div class="flex items-center space-x-2">
        <input type="checkbox" bind:checked={battleye} />
        <label>Battleye Enabled</label>
      </div>

      <div>
        <label class="font-semibold">Verify Signatures</label>
        <select bind:value={verifySignatures} class="mt-1 w-full border rounded p-2">
          <option value="0">0 - Disabled</option>
          <option value="1">1 - Check signatures</option>
          <option value="2">2 - Strict</option>
          <option value="3">3 - Very strict</option>
        </select>
      </div>

      <div>
        <label class="font-semibold">MOTD</label>
        <textarea bind:value={motd} class="mt-1 w-full border rounded p-2 h-28"></textarea>
      </div>

      <div class="flex space-x-4 mt-4">
        <a href="/mods" class="px-4 py-2 rounded bg-blue-500 text-white">Manage Mods</a>
        <a href="/missions" class="px-4 py-2 rounded bg-blue-500 text-white">Manage Missions</a>
      </div>

      <div>
        <label class="font-semibold">Preset Save Name</label>
        <input bind:value={presetName} class="mt-1 w-full border rounded p-2" />
      </div>

      <button on:click={saveSettings} class="w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded mt-6 text-lg font-semibold">
        Save Settings
      </button>
    </div>
  </div>
</div>

{#if showModal}
  <div class="fixed inset-0 flex items-center justify-center bg-opacity-50 backdrop-blur-xs z-50">
    <div class="bg-white rounded-xl shadow-lg p-6 max-w-sm w-full text-center" transition:fly="{{ y: -50, duration: 400 }}">
      <h2 class="text-xl font-semibold mb-4">Settings Saved!</h2>
      <p>Your server settings have been successfully saved.</p>
      <button
        on:click={() => showModal = false} 
        class="mt-6 px-4 py-2 bg-green-600 hover:bg-green-700  text-white rounded">
        Close
      </button>
    </div>
  </div>
{/if}