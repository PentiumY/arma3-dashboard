<script>
  import { onMount } from 'svelte';
  import Fuse from 'fuse.js';
  import Header from '$lib/components/Header.svelte';
  import api from '$lib/api';

  let mods = [];
  let searchQuery = '';
  let sortedBy = 'name';
  let selectedModlistFile;
  let presetTab = 'list';
  let selectedPreset = "test"

  let modPresets = [];
  let selectedMods = []; // Array of currently selected mod names

  onMount(async () => {
    selectedPreset = await api.get('current');
    mods = await api.get('allMods');
    modPresets = await api.get('presets');
    selectedMods = await api.get(`presets/${selectedPreset}/modlist`);
  });

  $: fuse = new Fuse(mods, { keys: ['name'], threshold: 0.4 });
  $: filteredMods = searchQuery ? fuse.search(searchQuery).map(r => r.item) : mods;
  $: sortedMods = filteredMods.slice().sort((a, b) => {
    if (sortedBy === 'name') return a.name.localeCompare(b.name);
    if (sortedBy === 'filesize') return b.filesize - a.filesize;
  });

  function toggleModSelection(modName) {
    if (selectedMods.includes(modName)) {
      selectedMods = selectedMods.filter(name => name !== modName);
    } else {
      selectedMods = [...selectedMods, modName];
    }
  }

  async function uploadModlist() {
    if (!selectedModlistFile) return;

    const formData = new FormData();
    formData.append('file', selectedModlistFile); // matches FastAPI param "file"

    const data = await api.post('upload', formData, true)

    if (data.modlist) {
        // Set selectedMods to only the names returned from backend
        console.log(data.modlist);
        selectedMods = data.modlist
        //selectedMods = data.mods.map(mod => mod.name);
    }
  }

  async function selectModPreset(preset) {
    presetTab = "list"
    selectedPreset = preset
    selectedMods = await api.get(`presets/${selectedPreset}/modlist`);
    await api.post('setCurrent', { name: selectedPreset });
  }

  async function saveSelectedMods() {
    // Send currently selected mods to backend
    await api.post(`presets/${selectedPreset}/modlist`, {
      modlist: selectedMods
    })

    alert('Selected mods saved.');
  }
</script>

<Header current="/mods" />

<div class="min-h-screen bg-gray-100 p-6">
  <div class="max-w-6xl mx-auto bg-white shadow rounded-xl p-6">
    <h1 class="text-3xl font-bold mb-6">Manage Mods</h1>

    <div class="flex space-x-4 mb-6">
      <button class="px-4 py-2 rounded bg-gray-800 text-white" on:click={() => presetTab = 'list'}>Local Mods</button>
      <button class="px-4 py-2 rounded bg-gray-800 text-white" on:click={() => presetTab = 'presets'}>Modlist Presets</button>
    </div>

    <div class="flex space-x-4 mb-6">
      <p>Current Preset: {selectedPreset}</p>
    </div>

    {#if presetTab === 'list'}
      <div class="mb-4 flex space-x-4">
        <input type="text" placeholder="Search mods..." bind:value={searchQuery} class="border rounded p-2 w-full" />
        <select bind:value={sortedBy} class="border rounded p-2">
          <option value="name">Sort by Name</option>
          <option value="filesize">Sort by File Size</option>
        </select>
      </div>
      
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b">
            <th class="py-2 px-4">Select</th>
            <th class="py-2 px-4">Name</th>
            <th class="py-2 px-4">File Size</th>
          </tr>
        </thead>
        <tbody>
          {#each sortedMods as mod}
            <tr class="border-b hover:bg-gray-50">
              <td class="py-2 px-4 text-center">
                <input type="checkbox" checked={selectedMods.includes(mod.name)} on:change={() => toggleModSelection(mod.name)} />
              </td>
              <td class="py-2 px-4">{mod.name}</td>
              <td class="py-2 px-4">{mod.filesize >= 1024 ? `${(mod.filesize/1024).toFixed(2)} GB` : `${mod.filesize.toFixed(2)} MB`}</td>
            </tr>
          {/each}
        </tbody>
      </table>

      <div class="mt-6 flex flex-col space-y-4">
        <label class="block font-semibold">Upload Modlist</label>
        <input type="file" accept=".html" on:change="{e => selectedModlistFile = e.target.files[0]}" />
        
        <button 
            on:click={uploadModlist} 
            class="px-4 py-2 rounded text-white"
            class:bg-green-600={selectedModlistFile} 
            class:hover:bg-green-700={selectedModlistFile} 
            class:bg-gray-400={!selectedModlistFile}   
            disabled={!selectedModlistFile} >
            Upload & Apply
        </button>
        
        <button on:click={saveSelectedMods} class="px-4 py-2 bg-blue-600 text-white rounded">
            Save Selected Mods
        </button>
      </div>
    {/if}

    {#if presetTab === 'presets'}
      <div>
        <h2 class="text-xl font-semibold mb-4">Local Modlist Presets</h2>
        <ul class="space-y-2">
          {#each modPresets as preset}
              <!-- svelte-ignore a11y_click_events_have_key_events -->
              <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
              <li on:click={() => selectModPreset(preset)}  class="p-4 border rounded hover:bg-gray-50 cursor-pointer">{preset}</li>
          {/each}
        </ul>
      </div>
    {/if}
  </div>
</div>
