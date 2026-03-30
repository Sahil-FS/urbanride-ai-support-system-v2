export type Message = {
  id: string;
  role: "user" | "bot";
  message: string;
  options?: { label: string; intent: string }[];
};