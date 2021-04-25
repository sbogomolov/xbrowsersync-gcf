# xBrowserSync API implementation using Google Cloud Functions

This is a simple implementation of the [xBrowserSync API](https://github.com/xbrowsersync/api) using Google Cloud Functions. It uses Firestore as a backend and Cloud Runtime Configuration for configuration.

## Deployment

### Using Terraform

Check this repository: [xbrowsersync-gcf-terraform](https://github.com/sbogomolov/xbrowsersync-gcf-terraform)

### Manual deployment

- Create a GCP Project
- Enable Firestore (e.g. by creating an application in App Engine)
- Create Cloud Runtime Configuration with one variable:
    - accept_new_syncs = "true"
- Zip the code of this repository and create two Cloud Functions (name and endpoint are the same):
    - info
    - bookmarks
- Pass the name of your Cloud Runtime Configuration you have created to functions as environment variable `RUNTIME_CONFIG_NAME`.

## Usage

Point your xBrowserSync plugin/app to the following URL:
```
https://us-central1-<GCP_PROJECT_ID>.cloudfunctions.net
```

Currently only `us-central1` region is available for Google Cloud Functions. If you will use another one, adjust the URL accordingly.

To disable new syncs you need to set `accept_new_syncs` to `false` (no need to redeploy functions):
```sh
gcloud beta runtime-config configs variables set accept_new_syncs false --config-name=<YOUR_CONFIGURATION_NAME> --is-text
```

## Disclaimer

This code is provided "as is" without any warranties nor guarantees. Author will not take any responsibility for anything related or unrelated to the usage of this code.
