{
  description = "Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};

        # Shared Python environment for the app and the dev shell
        pythonEnv = pkgs.python3.withPackages (ps:
          with ps; [
            beautifulsoup4
            debugpy
            requests
            scapy # this is for the network scanning
            simple-term-menu
            tkinter
            tqdm
          ]);

        # Only copy .py files into the Nix store (keeps .env and other junk out)
        src = ./.;

        gui = pkgs.writeShellApplication {
          name = "myapp";
          runtimeInputs = [pythonEnv];
          text = ''
            exec python ${src}/main.py "$@"
          '';
        };

        cli = pkgs.writeShellApplication {
          name = "myapp-cli";
          runtimeInputs = [pythonEnv];
          text = ''
            exec python ${src}/main.py --cli "$@"
          '';
        };
      in {
        packages = {
          default = gui;
          inherit gui cli;
        };

        apps = {
          default = {
            type = "app";
            program = "${gui}/bin/myapp";
            meta.description = "Run the app in GUI mode";
          };
          cli = {
            type = "app";
            program = "${cli}/bin/myapp-cli";
            meta.description = "Run the app in CLI mode";
          };
        };

        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv
            pkgs.git
          ];

          shellHook = ''
            # import env from env file
            if [ -f .env ]; then
              source ./.env
            else
              echo "No .env file found. Continuing without extra environment variables."
            fi

            echo "All packages ready"
          '';
        };
      }
    );
}
