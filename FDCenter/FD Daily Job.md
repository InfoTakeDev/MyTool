# FD Daily Job

## Gernal Check

Let's use Berwick(7.0.510) as an example

- Check the GI build Status
  - Check GI build result in Jenkins
  - Check the Cobump result (although the email said it's fail, but you have to check on it again)
- Check the "microservice-release"
  - Is there any pendding PR
- Check VIBs and Platform services version
  - Check if new VIBs ready for VV to test
  - Check if VIBs and Platform service in the GI

## Advanced information

### GI Build

- Get the Jenkins build result
  - provide the link of the jenkins

### for cobump

- If we have only one fail and more than 3 success in the same build.
Maybe we don't have to report it.
  - how to define it

### microservice-release

- Is the tag in microservice-release exist in the repo
- The difference between the current tag and the latest repo tag
- When is the current tag be tagged.

### vibs and platform service

- Get the latest VIBs and Platform service build.
- compare between VIBS build, VIBs in GI and config in the repo (from poxio)

### Sanity Result

- provide the sanity result
  - provide the link
  - what's the pass criterial of Pass or Fail.
  -

### auto taging
