#!/bin/bash

# stop instances
docker stop prod

# destroy instance
docker rm prod
