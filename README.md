# OpenMDX

Open Medical Diagnosis Explorer

# Backend Dev

# Frontend Dev

Install deno by following instructions at https://docs.deno.com/runtime/getting_started/installation/

Then, go to web and install:

```bash
cd web
deno install
```

Create a .env file with all the settings, change the settings related to keys.
```bash
cp dotenv.tpl .env
```

Then, start dev server

```bash
deno run --env-file vite
```