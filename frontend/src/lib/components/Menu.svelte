<script lang="ts">
  let mods = ['mod1', 'mod2', 'mod3'];
  let selected = [];

  function toggleMod(mod: string) {
    if (selected.includes(mod)) {
      selected = selected.filter(m => m !== mod);
    } else {
      selected = [...selected, mod];
    }
  }

  async function loadMods() {
    await fetch('/api/load-mods', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({mods: selected})
    });
    alert('Mods loaded!');
  }
</script>

<div class="p-4">
  <h2 class="font-bold text-lg mb-2">Select Mods</h2>
  <div class="flex flex-wrap gap-2">
    {#each mods as mod}
      <button
        class="px-3 py-1 rounded border border-gray-400 hover:bg-gray-700 transition"
        class:selected={selected.includes(mod)}
        on:click={() => toggleMod(mod)}
      >
        {mod}
      </button>
    {/each}
  </div>
  <button
    class="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      on:click={loadMods}
    >
    Load Selected Mods
  </button>
</div>

<style>
  .selected {
    background-color: #2563eb;
    color: white;
  }
</style>
