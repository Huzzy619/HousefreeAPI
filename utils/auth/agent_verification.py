import asyncio
import httpx



async def agent_identity_verification(
    front_image, back_image, selfie_image
):

    id = '71527f40-931d-11ed-9c25-97af89cddc4a '
    email = 'akinolatolulope24@gmail.com'
    body = {
        'client_id': id,
        'email': email
    }
    async with httpx.AsyncClient() as client:

        get_token = await client.post(
            url='https://app.faceki.com/getToken',
            json=body, timeout=None
        )
        body = {
            "doc_front_image": front_image,
            "doc_back_image": back_image,
            "selfie_image": selfie_image
        }

        if get_token.json():
            token = get_token.json()['token']
            
            verify_agent_details = await client.post(
                url='https://app.faceki.com/kyc-verification',
                headers={
                    "Authorization": f"Bearer {token}"
                },
                files=body,
                timeout=None
            )

            verify_agent_details = verify_agent_details.json()
            print('hello \n', verify_agent_details)
            status = verify_agent_details.get('status', '')
            if status:
                return None

            return verify_agent_details

        return None

