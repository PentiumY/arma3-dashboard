<script>
  export let current = '';

  const links = [
    { name: 'Server Config', href: '/config' },
    { name: 'Server Control', href: '/control' },
    { name: 'Mods', href: '/mods' },
    { name: 'Missions', href: '/missions' },
    { name: 'Logs', href: '/logs' }
  ];
</script>

<nav class="w-full bg-gray-900 text-white shadow-md">
  <div class="max-w-6xl mx-auto px-6 py-4 flex items-center space-x-6">
    <h1 class="text-2xl font-bold mr-6">Arma 3 Dashboard</h1>

    {#each links as link}
      <a
        href={link.href}
        class="px-3 py-2 rounded hover:bg-gray-700 transition"
        class:bg-gray-700={current === link.href}
      >
        {link.name}
      </a>
    {/each}
  </div>
</nav>