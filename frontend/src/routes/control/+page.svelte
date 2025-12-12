<script>
  import { onMount } from 'svelte';
    import Header from '$lib/components/Header.svelte';
  let cpu = 0;
  let memory = 0;
  let serverRunning = false;

  async function fetchStats() {
    const res = await fetch('/api/stats');
    const data = await res.json();
    cpu = data.cpu;
    memory = data.memory;
    serverRunning = data.running;
  }

  async function toggleServer() {
    await fetch(`/api/${serverRunning ? 'stop' : 'start'}`, { method: 'POST' });
    await fetchStats();
  }

  onMount(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 3000);
    return () => clearInterval(interval);
  });
</script>

<Header current="/control" />


<div class="min-h-screen bg-gray-100 p-6">
  <div class="max-w-4xl mx-auto bg-white shadow rounded-xl p-6 space-y-6">
    <h1 class="text-3xl font-bold mb-4">Arma 3 Control Panel</h1>

    <div class="flex items-center justify-between">
      <button
        class="px-6 py-3 text-white rounded text-lg font-semibold shadow"
        class:bg-green-600={!serverRunning}
        class:bg-red-600={serverRunning}
        on:click={toggleServer}
      >
        {serverRunning ? 'Stop Server' : 'Start Server'}
      </button>

      <a href="/logs" class="px-6 py-3 bg-blue-500 text-white rounded text-lg font-semibold shadow">
        View Logs
      </a>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
      <div class="bg-gray-50 p-6 rounded-xl shadow flex flex-col items-center">
        <h2 class="text-xl font-semibold mb-4">CPU Load</h2>
        <div class="w-40 h-40 rounded-full border-8 border-gray-300 relative">
          <div class="absolute inset-0 flex items-center justify-center text-2xl font-bold">{cpu}%</div>
          <div class="absolute inset-0 rounded-full border-8 border-green-500" style="clip-path: polygon(50% 0%, 100% 100%, 0% 100%);"></div>
        </div>
      </div>

      <div class="bg-gray-50 p-6 rounded-xl shadow flex flex-col items-center">
        <h2 class="text-xl font-semibold mb-4">Memory Usage</h2>
        <div class="w-40 h-40 rounded-full border-8 border-gray-300 relative">
          <div class="absolute inset-0 flex items-center justify-center text-2xl font-bold">{memory}%</div>
          <div class="absolute inset-0 rounded-full border-8 border-blue-500" style="clip-path: polygon(50% 0%, 100% 100%, 0% 100%);"></div>
        </div>
      </div>
    </div>
  </div>
</div>
