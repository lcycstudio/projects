import React from 'react';

import CustomLayout from './Layout';

class EmailVerify extends React.Component {
    render() {
        return (
            <CustomLayout>
                <h1 style={{ textAlign: 'center', padding: 24 }}> Account Email Verification </h1>
                <p> We have sent an e-mail to you for verification. Follow the link provided in the email to finalize the signup process. Please contact us if you do not receive it within a few minutes. </p>
            </CustomLayout>
        )
    }
};

export default EmailVerify;