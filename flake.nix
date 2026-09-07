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
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            (python3.withPackages (ps:
              with ps; [
                debugpy
              ]))
            git
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
