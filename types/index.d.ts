interface CustomMatchers<R = unknown> {
   /**
     * Use `.toBeAfter` when checking if a date occurs after `date`.
     * @param {Date} date
     */
    toBeSameStory(date: Date): R;
}

declare namespace jest {
  type Expect = CustomMatchers
  type Matchers<R> = CustomMatchers<R>
  type InverseAsymmetricMatchers = CustomMatchers
}