import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Auth } from 'aws-amplify';
import LoginPage from './LoginPage';

jest.mock('aws-amplify');

describe('LoginPage', () => {
  it('submits the form with username and password', async () => {
    Auth.signIn.mockResolvedValue({ username: 'testuser', password: 'testpass' });

    const { getByLabelText, getByRole } = render(<LoginPage />);

    userEvent.type(getByLabelText(/username/i), 'testuser');
    userEvent.type(getByLabelText(/password/i), 'testpass');

    fireEvent.click(getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(Auth.signIn).toHaveBeenCalledWith('testuser', 'testpass');
    });
  });
});