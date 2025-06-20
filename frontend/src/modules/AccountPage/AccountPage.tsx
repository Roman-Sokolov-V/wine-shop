import React, { useState } from 'react';
import {
  Box,
  Columns,
  Container,
  Content,
  Heading,
  Tag,
} from 'react-bulma-components';

interface UserData {
  firstName: string;
  lastName: string;
  email: string;
  is_staff: boolean;
}

export const AccountPage = () => {
  const [user] = useState<UserData>({
    firstName: 'Alex',
    lastName: 'Doe',
    email: 'alex.doe@example.com',
    is_staff: true,
  });

  return (
    <Container className="mt-6">
      <Columns centered>
        <Columns.Column size="half">
          <Box>
            <Heading size={3}>My Account</Heading>
            <hr />
            <Content>
              <Columns>
                <Columns.Column>
                  <p>
                    <strong>First Name:</strong>
                    <br />
                    {user.firstName}
                  </p>
                </Columns.Column>
                <Columns.Column>
                  <p>
                    <strong>Last Name:</strong>
                    <br />
                    {user.lastName}
                  </p>
                </Columns.Column>
              </Columns>

              <p>
                <strong>Email:</strong>
                <br />
                {user.email}
              </p>

              <p>
                <strong>Account Type:</strong>
                <br />
                {user.is_staff ? (
                  <Tag
                    color="success"
                    className="mt-1"
                  >
                    Staff Member
                  </Tag>
                ) : (
                  <Tag
                    color="info"
                    className="mt-1"
                  >
                    User
                  </Tag>
                )}
              </p>
            </Content>
          </Box>
        </Columns.Column>
      </Columns>
    </Container>
  );
};
