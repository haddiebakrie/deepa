import type { NextApiRequest, NextApiResponse } from 'next'
 
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const data = req.body
  const response = await fetch(
    "http://127.0.0.1:8000/signup",
    {
        method: "POST",
        body: data
    }
  )

  console.log(response.json())

}