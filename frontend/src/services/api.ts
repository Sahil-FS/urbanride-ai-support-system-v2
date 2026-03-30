export const sendChatMessage = async (message: string) => {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/v1/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message, user_id: 1 }),
    });

    if (!res.ok) throw new Error("API error");

    const data = await res.json();

    if (!data || !data.message) return null;

    return data;
  } catch (err) {
    console.error(err);
    return null;
  }
};