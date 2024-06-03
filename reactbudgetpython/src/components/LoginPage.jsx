import React, { useState } from 'react';
import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails
} from 'amazon-cognito-identity-js';
import AWS from 'aws-sdk';
import { awsconfig } from '../awsconfig.json'; // make sure this file contains your AWS configuration

// Configure the AWS SDK with your region
AWS.config.update({ region: awsconfig.aws_project_region });

const userPool = new CognitoUserPool({
  UserPoolId: awsconfig.aws_user_pools_id,
  ClientId: awsconfig.aws_user_pools_web_client_id,
});

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [user, setUser] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();

    const authenticationDetails = new AuthenticationDetails({
      Username: username,
      Password: password,
    });

    const cognitoUser = new CognitoUser({
      Username: username,
      Pool: userPool,
    });

    cognitoUser.authenticateUser(authenticationDetails, {
      onSuccess: (result) => {
        // The user object contains information about the signed-in user.
        setUser(cognitoUser);
        console.log(result);
      },
      onFailure: (error) => {
        console.log('Error signing in', error);
        // Handle sign-in errors here.
      },
    });
  };

  const handleSignOut = () => {
    if (user) {
      user.signOut();
      setUser(null);
    }
  };

  return (
    <div className="login-page">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label>
          Password:
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <input type="submit" value="Submit" />
      </form>
      {user && (
        <div>
          <h3>Hello {user.getUsername()}</h3>
          <button onClick={handleSignOut}>Sign out</button>
        </div>
      )}
    </div>
  );
};

export default LoginPage;
