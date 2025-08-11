import { GoogleGenAI } from "@google/genai";
import type { InventoryItem } from "../types";

export const fetchAIInsights = async (inventoryData: InventoryItem[]): Promise<string> => {
  try {
    if (!process.env.API_KEY) {
        throw new Error("API_KEY environment variable not set");
    }
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
    
    const prompt = `
      You are a senior business analyst. Analyze the following campaign inventory data (in JSON format) 
      and provide a concise summary of key insights. The data provided might be a filtered subset of a larger dataset.
      Focus on: 
      - Total potential revenue vs. booked revenue within the provided data.
      - The most valuable booked client or slot in this dataset.
      - Urgent opportunities (on-hold items that might need follow-up).
      - Upcoming available slots that should be prioritized for selling.
      - If the dataset is empty, state that there is no data to analyze for the current selection.
      Present the insights as a short introductory paragraph followed by a bulleted list using markdown.

      Data:
      ${JSON.stringify(inventoryData, null, 2)}
    `;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
    });
    
    return response.text;
  } catch (error) {
    console.error("Error fetching AI insights:", error);
    // Re-throw the error to be caught by the calling function
    throw new Error("Failed to generate insights from the AI service.");
  }
};
