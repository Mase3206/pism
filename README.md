# Post-Install Setup Masterscript

I had a bunch of separate shell scripts sitting in my homelab's internal wiki that I'd use when setting up a new LXC. These worked fine, but they were a pain in the butt to maintain, and I'm not a big fan of Bash scripting. 

This program seeks to simplify that process. It attempts to automatically detect the Linux distro it's running on and match it to a known list of distros and package managers. It then obfuscates the actual commands being run to make scripting much easier, simpler, and cleaner. 

## Usage

By default, `pism` runs interactively, asking a couple of questions as it goes. It will then confirm whether or not you would like to proceed with the setup. Refer to the following table for its command line options:

| Option | Description |
| :---: | :---- |
| `--non-interactive` | Runs in the non-interactive mode. All options passed in via CLI are final. |
| `--docker` | Installs Docker CE as part of the setup. |