/**
 * DO NOT CHANGE. This file is being managed from a central repository
 * To know more simply visit https://github.com/honestbank/.github/blob/main/docs/about.md
 */

class SemanticReleaseError extends Error {
    constructor(message, code, details) {
        super();
        Error.captureStackTrace(this, this.constructor);
        this.name = "SemanticReleaseError"
        this.details = details;
        this.code = code;
        this.semanticRelease = true;
    }
}

const getTestDockerImageName = () => `${process.env.DOCKER_REPO_TEST}`
const getProdDockerImageName = () => `${process.env.DOCKER_REPO_PROD}`

module.exports = {
    branches: [{name: 'main'}],
    verifyConditions: [
        () => {
            if (!process.env.DOCKER_REPO_TEST) {
                throw new SemanticReleaseError(
                    "No DOCKER_REPO_TEST specified",
                    "ENODOCKER_REPO_TEST",
                    "Please make sure you're logged in to docker and a repo is available to push to"
                );
            }
            if (!process.env.DOCKER_REPO_PROD) {
                throw new SemanticReleaseError(
                    "No DOCKER_REPO_PROD specified",
                    "ENODOCKER_REPO_PROD",
                    "Please make sure you're logged in to docker and a repo is available to push to"
                );
            }
        },
        "@semantic-release/github"
    ],
    prepare: [
        {
            path: "@semantic-release/exec",
            cmd: `docker build . --build-arg VERSION=\${nextRelease.version} -t ${getTestDockerImageName()}:\${nextRelease.version}`
        },
        {
            path: "@semantic-release/exec",
            cmd: `docker tag ${getTestDockerImageName()}:\${nextRelease.version} ${getTestDockerImageName()}:latest`
        },
        {
            path: "@semantic-release/exec",
            cmd: `docker tag ${getTestDockerImageName()}:\${nextRelease.version} ${getProdDockerImageName()}:\${nextRelease.version}`
        },
        {
            path: "@semantic-release/exec",
            cmd: `docker tag ${getTestDockerImageName()}:\${nextRelease.version} ${getProdDockerImageName()}:latest`
        },
    ],
    publish: [
        {
            path: "@semantic-release/exec",
            cmd: `docker push ${getProdDockerImageName()}:\${nextRelease.version}`
        },
        {
            path: "@semantic-release/exec",
            cmd: `docker push ${getProdDockerImageName()}:latest`
        },
        "@semantic-release/github"
    ],
};