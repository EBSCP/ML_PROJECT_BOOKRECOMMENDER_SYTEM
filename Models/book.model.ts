export interface Book {
  ISBN: string;
  Title: string;
  Author: string;
  Year: string;
  Publisher: string;
  est_rating: number;
  [key: string]: string | number; // Dinamik olarak yeni özelliklere izin verir
}
